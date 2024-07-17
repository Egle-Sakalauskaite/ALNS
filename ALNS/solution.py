class Solution:
    """Solution object that contains routes"""
    def __init__(self, data):
        """Initializes a new empty solution object
        :param data: data object of the current instance"""
        self.data = data
        self.routes = []

    @property
    def total_distance(self):
        """Calculates the total distance as the sum of all route distances"""
        dist = 0
        for route in self.routes:
            dist += route.distance
        return dist

    @property
    def total_battery_degradation_cost(self):
        """the total battery degradation cost as the sum of these costs of all routes"""
        cost = 0
        for route in self.routes:
            cost += route.battery_degradation_costs
        return cost

    @property
    def total_cost(self):
        """total cost as the sum of distance and battery degradation costs"""
        return self.total_distance + self.total_battery_degradation_cost

    @property
    def customer_visits(self):
        """Returns a list of all customer visits and the routes where they occurred
        :return a list of customer visits"""
        visits = []
        for route in self.routes:
            for visit in route.visits:
                if self.data.type[visit.loc] == "c":
                    visits.append((route, visit))
        return visits

    @property
    def source_visits(self):
        """Returns a list of all source visits and the routes where they occurred
        :return a list of source visits"""
        visits = []
        for route in self.routes:
            for visit in route.visits:
                if self.data.type[visit.loc] == "f":
                    visits.append((route, visit))
        return visits

    @property
    def is_feasible(self):
        """Solution is feasible if all routes are feasible"""
        for route in self.routes:
            if not route.is_feasible:
                return False
        return True

    @property
    def is_battery_feasible(self):
        """Solution is battery feasible if all routes are battery feasible"""
        for route in self.routes:
            if not route.is_battery_feasible:
                return False
        return True

    @property
    def all_customers_visited(self):
        """Returns true if all customers were visited, false otherwise"""
        return len(self.customer_visits) == self.data.n_customer

    def add_route(self, route):
        """Adds a route to the solution
        :param route: route object to insert"""
        self.routes.append(route)

    def remove_route(self, route):
        """Removes a route from the solution
        :param route: route object to remove
        :return the lists of visits of the removed route"""
        self.routes.remove(route)
        return route.visits

    def remove_empty_routes(self):
        """Removes all routes that do not contain any customer visits"""
        for route in self.routes:
            if len(route.visits) <= 2:
                self.routes.remove(route)