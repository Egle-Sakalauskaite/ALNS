import math


class LocationVisit:
    """Location visit objects that track time and vehicle state"""
    def __init__(self, data, loc, arrival_time, load_level_upon_arrival, battery_level_upon_arrival, charge_quantity=0):
        self.data = data
        self.loc = loc
        self.arrival_time = arrival_time
        self.battery_level_upon_arrival = battery_level_upon_arrival
        self.load_level_upon_departure = load_level_upon_arrival - self.data.demand[self.loc]
        self._charge_quantity = charge_quantity

    @property
    def departure_time(self):
        """sets departure time according to current arrival time"""
        if self.arrival_time < self.data.ready_time[self.loc]:
            start_time = self.data.ready_time[self.loc]
        else:
            start_time = self.arrival_time

        return start_time + self.data.service_time[self.loc] + self.data.recharging_rate * self.charge_quantity

    @property
    def battery_level_upon_departure(self):
        return self.battery_level_upon_arrival + self.charge_quantity

    @property
    def charge_quantity(self):
        return min(self._charge_quantity, self.data.battery_capacity - self.battery_level_upon_arrival)

    @charge_quantity.setter
    def charge_quantity(self, charge_quantity):
        if charge_quantity > 0 and self.data.type[self.loc] == "c":
            raise ValueError("Cannot charge at customer locations")

        if charge_quantity < 0:
            raise ValueError(f"charging quantity must be positive: {charge_quantity}")

        charge_quantity = min(charge_quantity, self.data.battery_capacity - self.battery_level_upon_arrival)

        self._charge_quantity = charge_quantity

    @property
    def is_feasible(self):
        """checks if the visit is feasible according to due time and vehicle load"""
        if self.arrival_time > self.data.due_time[self.loc]:
            return False
        if self.load_level_upon_departure < 0:
            return False

        return True

    @property
    def is_battery_feasible(self):
        """Checks if battery level drops below 0"""
        return self.battery_level_upon_arrival >= 0 or math.isclose(self.battery_level_upon_arrival, 0, abs_tol=1e-9)
    def update(self, new_arrival_time, load_level_difference, new_battery_level):
        self.arrival_time = new_arrival_time
        self.load_level_upon_departure += load_level_difference
        self.battery_level_upon_arrival = new_battery_level


