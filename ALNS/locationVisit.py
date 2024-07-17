import math
import config


class LocationVisit:
    """Location visit objects that track time and vehicle state"""
    def __init__(self, data, loc, arrival_time, load_level_upon_arrival, battery_level_upon_arrival, charge_quantity=0):
        """Initializes a new location visit
        :param data: data object of the current instance
        :param loc: location index
        :param arrival_time: arrival time to the location in minutes
        :param load_level_upon_arrival: load level when vehicle arrives
        :param battery_level_upon_arrival: battery level when vehicle arrives
        :param charge_quantity: charged quantity at the location (default value 0)"""
        self.data = data
        self.loc = loc
        self.arrival_time = arrival_time
        self.battery_level_upon_arrival = battery_level_upon_arrival
        self.load_level_upon_departure = load_level_upon_arrival - self.data.demand[self.loc]
        self._charge_quantity = charge_quantity

    @property
    def departure_time(self):
        """gets updated departure time"""
        if self.arrival_time < self.data.ready_time[self.loc]:
            start_time = self.data.ready_time[self.loc]
        else:
            start_time = self.arrival_time

        return start_time + self.data.service_time[self.loc] + self.data.recharging_rate * self.charge_quantity

    @property
    def battery_level_upon_departure(self):
        """gets updated battery level upon departure"""
        return self.battery_level_upon_arrival + self.charge_quantity

    @property
    def charge_quantity(self):
        """forbids the charged amount exceed batteries capacity"""
        return min(self._charge_quantity, self.data.battery_capacity - self.battery_level_upon_arrival)

    @charge_quantity.setter
    def charge_quantity(self, charge_quantity):
        """Charging is not allowed at customer locations
        charged quantity must be positive
        any attempted charge above batteries capacity will be reduced"""
        if charge_quantity > 0 and self.data.type[self.loc] == "c":
            raise ValueError("Cannot charge at customer locations")

        if charge_quantity < 0 and not math.isclose(charge_quantity, 0, abs_tol=1e-9):
            raise ValueError(f"charging quantity must be positive: {charge_quantity}")

        charge_quantity = min(charge_quantity, self.data.battery_capacity - self.battery_level_upon_arrival)

        self._charge_quantity = charge_quantity

    # Only for extension
    @property
    def battery_degradation_cost(self):
        """Returns the cost of battery degradation by considering the battery level on arrival and departure
         or 0 if the costs are not considered or if location is a customer"""
        if not config.BATTERY_DEGRADATION or self.data.type[self.loc] == "c":
            return 0
        else:
            under_LB = self.data.W_L * max(0, (self.data.LB - self.battery_level_upon_arrival))
            over_UB = self.data.W_H * max(0, self.battery_level_upon_departure - self.data.UB)
            return under_LB + over_UB

    @property
    def is_feasible(self):
        """visit is feasible if due time and vehicle load are not violated"""
        if self.arrival_time > self.data.due_time[self.loc]:
            return False
        if self.load_level_upon_departure < 0:
            return False

        return True

    @property
    def is_battery_feasible(self):
        """visit is feasible if battery level on arrival is above 0"""
        return self.battery_level_upon_arrival >= 0 or math.isclose(self.battery_level_upon_arrival, 0, abs_tol=1e-9)

    def update(self, new_arrival_time, load_level_difference, new_battery_level):
        """updates attributes: arrival time, load level upon departure, battery level upon arrival
        all other characteristics are properties and will be updated once accessed
        :param new_arrival_time: new time of arrival
        :param load_level_difference: increase (positive) or decrease (negative) in load level on arrival:
        :param new_battery_level: new battery level upon arrival
        """
        self.arrival_time = new_arrival_time
        self.load_level_upon_departure += load_level_difference
        self.battery_level_upon_arrival = new_battery_level
        self._charge_quantity = min(self._charge_quantity, self.data.battery_capacity - self.battery_level_upon_arrival)


    def print(self):
        """Prints all relevant information on this visit"""
        print(f"{self.loc}:")
        print(f"feasible? {self.is_feasible}")
        print(f"is battery feasible? {self.is_battery_feasible}")
        print(f"time window: [{self.data.ready_time[self.loc]} - {self.data.due_time[self.loc]}]")
        print(f"demand: {self.data.demand[self.loc]}")
        print(
            f"arrived: {self.arrival_time} (service: +{self.data.service_time[self.loc]} charging +{self.data.recharging_rate * self.charge_quantity}) - departure: {self.departure_time}")
        print(f"vehicle load: {self.load_level_upon_departure}")
        print(
            f"battery level: {self.battery_level_upon_arrival} (charged: +{self.charge_quantity})  - {self.battery_level_upon_departure}")
        print(f"battery degradation cost: {self.battery_degradation_cost}")

