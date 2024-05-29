class Solution:

    def __init__(self, data):
        self.data = data
        self.total_distance = 0
        self.routes = []

    def add_route(self, route):
        self.routes.append(route)
        self.total_distance += route.distance

    def remove_route(self, route):
        self.routes.remove(route)
        self.total_distance -= route.distance
        return route.visits

    @property
    def customer_visits(self):
        visits = []

        for route in self.routes:
            for visit in route.visits:
                if self.data.type[visit.loc] == "c":
                    visits.append((route, visit))

        return visits

    @property
    def source_visits(self):
        visits = []

        for route in self.routes:
            for visit in route.visits:
                if self.data.type[visit.loc] == "f":
                    visits.append((route, visit))

        return visits
