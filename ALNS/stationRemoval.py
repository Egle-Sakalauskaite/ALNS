import helper


class StationRemoval:
    def __init__(self, data, rnd):
        self.data = data
        self.rnd = rnd
        self.operations = [self.random_station_removal,
                           self.worst_distance_station_removal,
                           self.worst_charge_usage_station_removal,
                           self.full_charge_station_removal]
        self.times_used = []
        self.weights = [1 for _ in range(len(self.operations))]
        self.scores = {}

        for operation in self.operations:
            self.scores[operation] = 0

    # SR operations
    def random_station_removal(self, n_s, solution):
        for i in range(n_s):
            selected_route, selected_visit = self.rnd.choice(solution.customer_visits)
            selected_route.remove_visit(selected_visit)

    def worst_distance_station_removal(self, n_s, solution):
        determinism_factor = 4
        removal_costs = []

        for route in solution.routes:
            for i, visit in enumerate(route.visits):
                if self.data.type[visit.loc] != "c":
                    continue

                pred = route.visits[i - 1].loc
                suc = route.visits[i + 1].loc
                costs = self.data.distance_between(visit.loc, pred) + self.data.distance_between(visit.loc, suc)
                removal_costs.append((route, visit, costs))

        removal_costs.sort(key=lambda x: x[2], reverse=True)

        for i in range(n_s):
            removal_index = int(len(removal_costs) * (self.rnd.random() ** determinism_factor))
            route, visit, cost = removal_costs.pop(removal_index)
            route.remove_visit(visit)


    def worst_charge_usage_station_removal(self, n_s, solution):
        self.charge_station_removal(n_s, solution, lambda visit: visit.battery_level_upon_arrival)

    def full_charge_station_removal(self, n_s, solution):
        self.charge_station_removal(n_s, solution, lambda visit: visit.battery_level_upon_departure)

    # general methods
    def charge_station_removal(self, n_s, solution, costs_func):
        costs = []

        for route in solution.routes:
            for i, visit in enumerate(route.visits):
                if self.data.type[visit.loc] != "f":
                    continue

                costs = costs_func(visit)
                costs.append((route, visit, costs))

        costs.sort(key=lambda x: x[2], reverse=True)

        for i in range(n_s):
            route, visit, cost = costs.pop(0)
            route.remove_visit(visit)
