from locationVisit import LocationVisit
import helper
from reader import Reader
import copy

class Route:
    """Route objects that track all location visits in order"""

    def __init__(self, data):
        self.data = data
        self.visits = []
        self.distance = 0
        self.visits.append(LocationVisit(data, 0, 0, data.load_capacity, data.battery_capacity))
        self.visits.append(LocationVisit(data, 0, 0, data.load_capacity, data.battery_capacity))

    @property
    def first_battery_violation_idx(self):
        for i, visit in enumerate(self.visits):
            if not visit.is_battery_feasible:
                return i
        return -1

    @property
    def source_visit_idx(self):
        visit_idx = []
        for i, visit in enumerate(self.visits):
            if self.data.type[visit.loc] == "f":
                visit_idx.append(i)
        return visit_idx

    @property
    def required_charge(self):
        return self.distance * self.data.battery_consumption_rate - self.data.battery_capacity - self.total_charged_quantity

    def possible_charge_before_time_infeasible(self, idx):
        min_arrival_due_time_difference = 9999999999

        for visit in self.visits[idx:]:
            time_before_due_date = self.data.due_time[visit.loc] - visit.arrival_time
            if time_before_due_date < min_arrival_due_time_difference:
                min_arrival_due_time_difference = time_before_due_date

        return max(0, min_arrival_due_time_difference / self.data.recharging_rate)

    def insert_at(self, loc, idx):
        """inserts location loc after position in the route idx"""
        pred = self.visits[idx - 1]
        suc = self.visits[idx]

        distance_pred_to_loc = self.data.distance_between(pred.loc, loc)
        distance_pred_to_suc = self.data.distance_between(pred.loc, suc.loc)
        distance_loc_to_suc = self.data.distance_between(loc, suc.loc)
        change_in_distance = distance_pred_to_loc + distance_loc_to_suc - distance_pred_to_suc
        load_level_difference = -self.data.demand[loc]
        arrival_time = pred.departure_time + distance_pred_to_loc / self.data.velocity
        load_level_upon_arrival = pred.load_level_upon_departure
        battery_level_upon_arrival = pred.battery_level_upon_departure - self.data.battery_consumption_rate * distance_pred_to_loc
        self.distance += change_in_distance
        charge_quantity = 0

        if self.data.type[loc] == "f" and self.required_charge > 0:
            charge_quantity = self.required_charge

        if loc == pred.loc:
            pred.charge_quantity += charge_quantity
            idx -= 1
        elif loc == suc.loc:
            suc.charge_quantity += charge_quantity
            idx -= 1
        else:
            visit = LocationVisit(self.data, loc, arrival_time, load_level_upon_arrival, battery_level_upon_arrival, charge_quantity)
            self.visits.insert(idx, visit)

        for i in range(idx + 1, len(self.visits)):
            self.update(i, load_level_difference)

        if self.data.type[loc] == "c":
            self.adjust_recharge(idx)

    def adjust_recharge(self, idx):
        source_visits = self.source_visit_idx

        if not self.is_battery_feasible and len(source_visits) > 0:
            recharge_at = source_visits[0]

            if len(source_visits) > 1:
                for source_visit in source_visits:
                    if source_visit < idx:
                        recharge_at = source_visit
                    else:
                        break

            self.visits[recharge_at].charge_quantity += self.required_charge
            for i in range(recharge_at + 1, len(self.visits)):
                self.update(i, 0)

            # time_feasible_recharge_quantity = min(self.possible_charge_before_time_infeasible(recharge_at), self.required_charge)
            # if time_feasible_recharge_quantity > 0:
            #     self.visits[recharge_at].charge_quantity += time_feasible_recharge_quantity
            #     # print(f"INCREASE THE CHARGE IN {self.visits[recharge_at].loc} by {time_feasible_recharge_quantity}")
            #     for i in range(recharge_at + 1, len(self.visits)):
            #         self.update(i, 0)


    def remove_visit(self, visit):
        idx = self.visits.index(visit)
        pred = self.visits[idx - 1]
        suc = self.visits[idx + 1]
        print(f"REMOVING: {pred.loc} - {visit.loc} - {suc.loc}")

        distance_pred_to_loc = self.data.distance_between(pred.loc, visit.loc)
        distance_pred_to_suc = self.data.distance_between(pred.loc, suc.loc)
        distance_loc_to_suc = self.data.distance_between(visit.loc, suc.loc)

        change_in_distance = distance_pred_to_suc - (distance_pred_to_loc + distance_loc_to_suc)
        load_level_difference = self.data.demand[visit.loc]
        self.distance += change_in_distance
        self.visits.remove(visit)

        for i in range(idx, len(self.visits)):
            self.update(i, load_level_difference)

        if self.data.type[visit.loc] == "c":
            self.remove_customer_with_succeeding_station(idx)
            self.remove_customer_with_preceding_station(idx)


    def remove_customer_with_preceding_station(self, removed_idx):
        if self.data.type[self.visits[removed_idx - 1].loc] == 'f':
            copied_route = copy.deepcopy(self)
            copied_route.remove_visit(copied_route.visits[removed_idx - 1])

            if copied_route.is_battery_feasible:
                print(f"removing unnecessary station visit")
                self.remove_visit(self.visits[removed_idx - 1])

    def remove_customer_with_succeeding_station(self, removed_idx):
        if self.data.type[self.visits[removed_idx].loc] == 'f':
            copied_route = copy.deepcopy(self)
            copied_route.remove_visit(copied_route.visits[removed_idx])

            if copied_route.is_battery_feasible:
                print(f"removing unnecessary station visit")
                copied_route.print()
                self.remove_visit(self.visits[removed_idx])

    def update(self, idx, load_level_difference):
        prev = self.visits[idx - 1]
        to_update = self.visits[idx]
        new_distance = self.data.distance_between(prev.loc, to_update.loc)
        new_arrival_time = prev.departure_time + new_distance / self.data.velocity
        new_battery_level = prev.battery_level_upon_departure - self.data.battery_consumption_rate * new_distance
        to_update.update(new_arrival_time, load_level_difference, new_battery_level)

    @property
    def total_charged_quantity(self):
        charged_quantity = 0

        for visit in self.visits:
            charged_quantity += visit.charge_quantity

        return charged_quantity

    @property
    def is_feasible(self):
        for visit in self.visits:
            if not visit.is_feasible:
                return False
        return True

    @property
    def is_battery_feasible(self):
        for visit in self.visits:
            if not visit.is_battery_feasible:
                return False
        return True

    def print(self):
        print("==============================================================")
        print(f"is feasible? {self.is_feasible}")
        print(F"is battery feasible? {self.is_battery_feasible}")
        print(f"total route distance: {self.distance}")
        print(f"total charged quantity: {self.total_charged_quantity}")
        current_loc = 0
        for visit in self.visits:
            loc = visit.loc

            distance = self.data.distance_between(current_loc, loc)
            current_loc = loc

            print(f"{loc}:")
            print(f"feasible? {visit.is_feasible}")
            print(f"is battery feasible? {visit.is_battery_feasible}")
            print(f"time window: [{self.data.ready_time[loc]} - {self.data.due_time[loc]}]")
            print(f"demand: {self.data.demand[loc]}")
            print(f"distance to: {distance}")
            print(
                f"arrived: {visit.arrival_time} (service: +{self.data.service_time[loc]} charging +{self.data.recharging_rate * visit.charge_quantity}) - departure: {visit.departure_time}")
            print(f"vehicle load: {visit.load_level_upon_departure}")
            print(
                f"battery level: {visit.battery_level_upon_arrival} (charged: +{visit.charge_quantity})  - {visit.battery_level_upon_departure}")

