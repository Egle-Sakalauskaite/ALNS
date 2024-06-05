class StationRemoval:
    """Operations for removing stations"""
    def __init__(self, data, rnd):
        self.data = data
        self.rnd = rnd
        self.operations = [self.random_station_removal,
                           self.worst_distance_station_removal,
                           self.worst_charge_usage_station_removal,
                           self.full_charge_station_removal]
        self.scores = {}
        self.weights = {}
        self.times_used = {}
        for operation in self.operations:
            self.scores[operation] = 0
            self.weights[operation] = 1 / len(self.operations)
            self.times_used[operation] = 0

    def station_removal(self, solution):
        n_s = self.get_n_to_remove(solution)
        # print(f"removing {n_s} stations")
        operation = self.choose_operation()
        operation(n_s, solution)
        return operation, solution

    # SR operations
    def random_station_removal(self, n_s, solution):
        """removes stations at random"""
        # print("SR: Random station removal")
        for i in range(n_s):
            selected_route, selected_visit = self.rnd.choice(solution.source_visits)
            selected_route.remove_visit(selected_visit)

    def worst_distance_station_removal(self, n_s, solution):
        """removes visits to the station that cause largest increase in distance"""
        # print("SR: Worst distance station removal")
        determinism_factor = 4
        removal_costs = []

        for route in solution.routes:
            for i, visit in enumerate(route.visits):
                if self.data.type[visit.loc] != "f":
                    continue

                pred = route.visits[i - 1].loc
                suc = route.visits[i + 1].loc
                costs = self.data.distance_matrix[visit.loc, pred] + self.data.distance_matrix[visit.loc, suc]
                removal_costs.append((route, visit, costs))

        removal_costs.sort(key=lambda x: x[2], reverse=True)

        for i in range(n_s):
            removal_index = int(len(removal_costs) * (self.rnd.random() ** determinism_factor))
            route, visit, cost = removal_costs.pop(removal_index)
            route.remove_visit(visit)


    def worst_charge_usage_station_removal(self, n_s, solution):
        """removes visits to the station where the vehicle arrives with largest charged quantity"""
        # print("SR: Worst charged usage station removal")
        self.charge_station_removal(n_s, solution, lambda visit: visit.battery_level_upon_arrival)

    def full_charge_station_removal(self, n_s, solution):
        """removes visits to the station where vehicle is charged to its capacity"""
        # print("SR; Full charged station removal")
        self.charge_station_removal(n_s, solution, lambda visit: visit.battery_level_upon_departure)

    # general methods
    def charge_station_removal(self, n_s, solution, costs_func):
        """general function for worst-charge-usage and full-charge station removal"""
        all_costs = []

        for route in solution.routes:
            for i, visit in enumerate(route.visits):
                if self.data.type[visit.loc] != "f":
                    continue

                cost = costs_func(visit)
                all_costs.append((route, visit, cost))

        all_costs.sort(key=lambda x: x[2], reverse=True)

        for i in range(n_s):
            route, visit, cost = all_costs.pop(0)
            route.remove_visit(visit)

    def get_n_to_remove(self, solution):
        n = len(solution.source_visits)
        LB = min(0.1 * n, 30)
        UB = min(0.4 * n, 60)
        return int(self.rnd.uniform(LB, UB))

    def choose_operation(self):
        """Randomly chooses a operation with probability reflected by the weights"""
        return self.rnd.choices(self.operations, weights=list(self.weights.values()), k=1)[0]

