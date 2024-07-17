import config


class StationRemoval:
    """Operations for removing stations"""
    def __init__(self, data, rnd):
        """initializes station removal scores and weights at the beginning of the ALNS
        :param data: the instance data from the Reader
        :param rnd: the RND used for this instance run"""
        self.data = data
        self.rnd = rnd
        self.operations = [self.random_station_removal,
                           self.worst_distance_station_removal,
                           self.worst_charge_usage_station_removal,
                           self.full_charge_station_removal]

        # Only for extension
        if config.BATTERY_DEGRADATION:
            self.operations.append(self.worst_battery_degradation_station_removal)

        self.scores = {}
        self.weights = {}
        self.times_used = {}
        for operation in self.operations:
            self.scores[operation] = 0
            self.weights[operation] = 1 / len(self.operations)
            self.times_used[operation] = 0

    def station_removal(self, solution):
        """Removes n_s stations from the solution
        :param solution: the current solution
        :return operation chosen and solution after removal"""
        n_s = self.get_n_to_remove(solution)
        operation = self.choose_operation()
        operation(n_s, solution)
        return operation, solution

    # SR operations
    def random_station_removal(self, n_s, solution):
        """removes stations at random
        :param n_s: the number of stations to be removed
        :param solution: the current solution"""
        for i in range(n_s):
            selected_route, selected_visit = self.rnd.choice(solution.source_visits)
            selected_route.remove_visit(selected_visit)

    def worst_distance_station_removal(self, n_s, solution):
        """removes visits to the station that cause largest increase in distance
        :param n_s: the number of stations to be removed
        :param solution: the current solution"""
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
        """removes visits to the station where the vehicle arrives with largest charged quantity
        :param n_s: the number of stations to be removed
        :param solution: the current solution"""
        # print("SR: Worst charged usage station removal")
        self.charge_station_removal(n_s, solution, lambda visit: visit.battery_level_upon_arrival)

    def full_charge_station_removal(self, n_s, solution):
        """removes visits to the stations where vehicle is charged to its capacity
        :param n_s: the number of stations to be removed
        :param solution: the current solution"""
        # print("SR; Full charged station removal")
        self.charge_station_removal(n_s, solution, lambda visit: visit.battery_level_upon_departure)

    def worst_battery_degradation_station_removal(self, n_s, solution):
        """Removes visits to the stations where largest battery degradation costs are endured
        :param n_s: the number of stations to be removed
        :param solution: the current solution"""
        self.charge_station_removal(n_s, solution, lambda visit: visit.battery_degradation_cost)

    # general methods
    def charge_station_removal(self, n_s, solution, costs_func):
        """general function for worst-charge-usage and full-charge station removal
        :param n_s: the number of stations to remove
        :param solution: the current solution
        :param costs_func: the costs function to be used"""
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
        """randomly selects a number of stations to remove
        :param solution: the current solution
        :return: the number of stations to remove"""
        n = len(solution.source_visits)
        LB = min(0.1 * n, 30)
        UB = min(0.4 * n, 60)
        return int(self.rnd.uniform(LB, UB))

    def choose_operation(self):
        """Randomly chooses a operation with probability reflected by the weights
        :return the operation chosen"""
        return self.rnd.choices(self.operations, weights=list(self.weights.values()), k=1)[0]

