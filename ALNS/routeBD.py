from locationVisit import LocationVisit
import copy

class Route:
    """Route objects that track all location visits in order"""
    def __init__(self, data):
        """Initializes an empty route that only has mandatory visits to the depot
        :param data: data object of the current instance"""
        self.data = data
        self.visits = []
        self.distance = 0
        self.visits.append(LocationVisit(data, 0, 0, data.load_capacity, data.UB))
        self.visits.append(LocationVisit(data, 0, 0, data.load_capacity, data.UB))

    @property
    def first_battery_violation_idx(self):
        """If any visit is battery infeasible, returns the position idx of the first such visit, -1 otherwise"""
        for i, visit in enumerate(self.visits):
            if not visit.is_battery_feasible:
                return i

        if self.visits[-1].battery_level_upon_arrival < self.data.LB:
            return len(self.visits) - 1

        return -1

    @property
    def total_charged_quantity(self):
        """Sums up all charged quantities of all the source visits"""
        charged_quantity = 0

        for visit in self.visits:
            charged_quantity += visit.charge_quantity

        return charged_quantity

    @property
    def required_charge(self):
        """Calculates the amount vehicle needs to be charged in order to reach the depot battery empty"""
        return max(0, self.distance * self.data.battery_consumption_rate - self.data.UB - self.total_charged_quantity + self.data.LB)

    @property
    def battery_degradation_costs(self, start_idx=0):
        """The costs of battery degradation as the sum of battery degradation costs of all visits"""
        costs = 0
        for i in range(start_idx, len(self.visits)):
            costs += self.visits[i].battery_degradation_cost
        return costs

    @property
    def total_cost(self):
        """total cost as the sum of distance cost and battery degradation cost"""
        return self.distance + self.battery_degradation_costs

    @property
    def is_feasible(self):
        """Route is feasible if all its location visits are feasible"""
        for visit in self.visits:
            if not visit.is_feasible:
                return False
        return True

    @property
    def is_battery_feasible(self):
        """Route is battery feasible if all its location visits are battery feasible"""
        for visit in self.visits:
            if not visit.is_battery_feasible:
                return False

        if self.visits[-1].battery_level_upon_arrival < self.data.LB:
            return False

        return True

    def get_last_source_visit(self, idx):
        """returns the most recent visit to the statiob for position idx
        :param idx: position index of the visit for which we look for last visit to the station
        :return: the route position idx of the most recent source visit"""
        for i in range(idx - 1, 0, -1):
            loc = self.visits[i].loc
            if self.data.type[loc] == 'f':
                return i
        return 0

    def possible_charge_before_time_infeasible(self, idx):
        """Checks what is the possible longest delay at position idx before some upcoming visit is time infeasible
        and calculates the possible largest charge quantity that can be obtained during that tim
        :param idx: position index of the visit for which the charging is considered
        :return: the quantity that can be charged before arriving to some customer becomes infeasible"""
        min_arrival_due_time_difference = 9999999999

        for visit in self.visits[idx:]:
            time_before_due_date = max(0, self.data.due_time[visit.loc] - visit.arrival_time)
            if time_before_due_date < min_arrival_due_time_difference:
                min_arrival_due_time_difference = time_before_due_date

        return min_arrival_due_time_difference / self.data.recharging_rate

    def insert_at(self, loc, idx=None):
        """inserts location loc at position idx
        :param loc: location index of insertion (which customer/station))
        :param idx: position index in the route where to make the insertion"""
        if idx == None:
            idx = len(self.visits) - 1

        pred = self.visits[idx - 1]
        suc = self.visits[idx]

        distance_pred_to_loc = self.data.distance_matrix[pred.loc, loc]
        distance_pred_to_suc = self.data.distance_matrix[pred.loc, suc.loc]
        distance_loc_to_suc = self.data.distance_matrix[loc, suc.loc]
        change_in_distance = distance_pred_to_loc + distance_loc_to_suc - distance_pred_to_suc
        load_level_difference = -self.data.demand[loc]
        arrival_time = pred.departure_time + distance_pred_to_loc / self.data.velocity
        load_level_upon_arrival = pred.load_level_upon_departure
        battery_level_upon_arrival = pred.battery_level_upon_departure - self.data.battery_consumption_rate * distance_pred_to_loc
        available_battery_space = self.data.battery_capacity - battery_level_upon_arrival
        self.distance += change_in_distance
        charge_quantity = 0

        if self.data.type[loc] == "f" and self.required_charge > 0:
            charge_quantity = min(self.required_charge, available_battery_space)

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
        """attempts to make the route battery feasible by increasing charge quantity in existing stations without causing time infeasibility
        :param idx: position index of the newly inserted location, for which recharging at an earlier visited station is considered"""
        if not self.is_battery_feasible:
            recharge_at = self.get_last_source_visit(idx)

            time_feasible_recharge_quantity = min(self.possible_charge_before_time_infeasible(recharge_at), self.required_charge)
            if time_feasible_recharge_quantity > 0:
                self.visits[recharge_at].charge_quantity += time_feasible_recharge_quantity
                # print(f"INCREASE THE CHARGE IN {self.visits[recharge_at].loc} by {time_feasible_recharge_quantity}")
                for i in range(recharge_at + 1, len(self.visits)):
                    self.update(i, 0)

    def remove_visit(self, visit):
        """Removes the visit from the route
        :param visit: the location visit object to remove"""
        idx = self.visits.index(visit)
        pred = self.visits[idx - 1]
        suc = self.visits[idx + 1]
        # print(f"REMOVING: {pred.loc} - {visit.loc} - {suc.loc}")

        distance_pred_to_loc = self.data.distance_matrix[pred.loc, visit.loc]
        distance_pred_to_suc = self.data.distance_matrix[pred.loc, suc.loc]
        distance_loc_to_suc = self.data.distance_matrix[visit.loc, suc.loc]

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
        """If removed customer was after a visit to the station which is no longer necessary
        that visit to the station is also removed
        :param: removed_idx: position index of the customer visit that was removed"""
        if self.data.type[self.visits[removed_idx - 1].loc] == 'f':
            copied_route = copy.deepcopy(self)
            copied_route.remove_visit(copied_route.visits[removed_idx - 1])

            if copied_route.is_battery_feasible:
                # print(f"removing unnecessary station visit")
                self.remove_visit(self.visits[removed_idx - 1])

    def remove_customer_with_succeeding_station(self, removed_idx):
        """If removed customer was before a visit to the station which is no longer necessary
        that visit to the station is also removed
        :param: removed_idx: position index of the customer visit that was removed"""
        if self.data.type[self.visits[removed_idx].loc] == 'f':
            copied_route = copy.deepcopy(self)
            copied_route.remove_visit(copied_route.visits[removed_idx])

            if copied_route.is_battery_feasible:
                # print(f"removing unnecessary station visit")
                self.remove_visit(self.visits[removed_idx])

    def update(self, idx, load_level_difference):
        """Updates following visits after location is inserted/removed at position idx
        :param: idx: position index of the inserted/removed visit
        :param: load_level_difference: inserted (negative)/ removed (positive) visit's demand"""
        prev = self.visits[idx - 1]
        to_update = self.visits[idx]
        new_distance = self.data.distance_matrix[prev.loc, to_update.loc]
        new_arrival_time = prev.departure_time + new_distance / self.data.velocity
        new_battery_level = prev.battery_level_upon_departure - self.data.battery_consumption_rate * new_distance
        to_update.update(new_arrival_time, load_level_difference, new_battery_level)

    def print(self):
        """Prints all the relevant information on this route and its location visits"""
        print("==============================================================")
        print(f"is feasible? {self.is_feasible}")
        print(F"is battery feasible? {self.is_battery_feasible}")
        print(f"total route distance: {self.distance}")
        print(f"total BD cost: {self.battery_degradation_costs}")
        print(f"total charged quantity: {self.total_charged_quantity}")
        current_loc = 0
        for visit in self.visits:
            loc = visit.loc
            distance = self.data.distance_matrix[current_loc, loc]
            current_loc = loc
            print(f"distance to: {distance}")
            visit.print()
