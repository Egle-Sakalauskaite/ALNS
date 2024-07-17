import math
import helper

class CustomerRemoval:
    """Operations for removing customers"""
    def __init__(self, data, rnd):
        """initializes customer removal scores and weights at the beginning of the ALNS
        :param data: the instance data from the Reader
        :param rnd: the RND used for this instance run"""
        self.data = data
        self.rnd = rnd
        self.operations = [self.random_removal,
                           self.worst_distance_removal,
                           self.worst_time_removal,
                           self.shaw_removal,
                           self.proximity_based_removal,
                           self.time_based_removal,
                           self.demand_based_removal,
                           self.zone_removal,
                           self.random_route_removal,
                           self.greedy_route_removal]
        self.scores = {}
        self.weights = {}
        self.times_used = {}

        for operation in self.operations:
            self.scores[operation] = 0
            self.weights[operation] = 1 / len(self.operations)
            self.times_used[operation] = 0

    def customer_removal(self, solution):
        """removes n_c customers from the current solution.
        :param solution: solution before removal
        :return: the operation that was used, a set of customers removed, solution after customer removal"""
        n_c = self.get_n_to_remove()
        operation = self.choose_operation()
        removed = operation(solution, n_c)

        return operation, removed, solution

    def route_removal(self, solution):
        """Removes a route from the current solution.
        :param solution: solution before removal
        :return: the operation that was used, a set of customers removed, solution after customer removal"""
        operation = self.choose_route_removal()
        removed = operation(solution)

        return operation, removed, solution

    # CR operations
    def random_removal(self, solution, n_c):
        """Removes customers at random
        :param solution: solution before removal
        :param n_c: number of customers to remove
        :return a set of removed customers"""
        removed = []

        for i in range(n_c):
            selected_route, selected_visit = self.rnd.choice(solution.customer_visits)
            selected_route.remove_visit(selected_visit)
            removed.append(selected_visit.loc)

        return removed

    def worst_distance_removal(self, solution, n_c):
        """Removes customers that cause the largest increase in distance
        :param solution: solution before removal
        :param n_c: number of customers to remove
        :return a set of removed customers"""
        def distance_costs(solution):
            removal_costs = []

            for route in solution.routes:
                for i, visit in enumerate(route.visits):
                    if self.data.type[visit.loc] != "c":
                        continue

                    pred = route.visits[i - 1].loc
                    suc = route.visits[i + 1].loc
                    costs = self.data.distance_matrix[visit.loc, pred] + self.data.distance_matrix[visit.loc, suc]
                    removal_costs.append((route, visit, costs))

            return removal_costs

        return self.costs_removal(n_c, 4, solution, distance_costs)

    def worst_time_removal(self, solution, n_c):
        """Removes customers that cause largest increase in time
        :param solution: solution before removal
        :param n_c: number of customers to remove
        :return a set of removed customers"""
        def time_costs(solution):
            removal_costs = []

            for route in solution.routes:
                for visit in route.visits:
                    if self.data.type[visit.loc] != "c":
                        continue

                    costs = abs(visit.arrival_time - self.data.ready_time[visit.loc])
                    removal_costs.append((route, visit, costs))

            return removal_costs

        return self.costs_removal(n_c, 4, solution, time_costs)

    def shaw_removal(self, solution, n_c):
        """Removes customers that are similar
        :param solution: solution before removal
        :param n_c: number of customers to remove
        :return a set of removed customers"""
        def shaw_costs(solution):
            return self.shaw_costs_general(solution, 0.5, 13, 0.15, 0.25)

        return self.costs_removal(n_c, 12, solution, shaw_costs)

    def proximity_based_removal(self, solution, n_c):
        """Shaw removal, but only proximity is considered
        :param solution: solution before removal
        :param n_c: number of customers to remove
        :return a set of removed customers"""
        def proximity_based_costs(solution):
            return self.shaw_costs_general(solution, 1, 0, 0, 0)

        return self.costs_removal(n_c, 12, solution, proximity_based_costs)

    def time_based_removal(self, solution, n_c):
        """Like Shaw removal, but only ready time difference is considered
        :param solution: solution before removal
        :param n_c: number of customers to remove
        :return a set of removed customers"""
        def time_based_costs(solution):
            return self.shaw_costs_general(solution, 0, 1, 0, 0)

        return self.costs_removal(n_c, 12, solution, time_based_costs)

    def demand_based_removal(self, solution, n_c):
        """Like Shaw removal, but only demand difference is considered
        :param solution: solution before removal
        :param n_c: number of customers to remove
        :return a set of removed customers"""
        def demand_based_costs(solution):
            return self.shaw_costs_general(solution, 0, 0, 0, 1)

        return self.costs_removal(n_c, 12, solution, demand_based_costs)

    def zone_removal(self, solution, n_c = 0):
        """Removes all customers in a random zone of the Cartesian plane
        :param solution: solution before removal
        :param n_c: number of customers to remove
        :return a set of removed customers"""
        removed = []
        zones = helper.split_into_zones(self.data, solution)

        while True:
            zone_to_remove = self.rnd.choice(list(zones.keys()))

            if len(zones[zone_to_remove]) > 0:
                break

        for route, visit in zones[zone_to_remove]:
            route.remove_visit(visit)
            removed.append(visit.loc)

        return removed

    def random_route_removal(self, solution, n_c = 0):
        """Removes a route at random
        :param solution: solution before removal
        :param n_c: set to 0 by default because not relevant
        :return a set of removed customers"""
        def random_selection(solution, n_routes_to_remove):
            return self.rnd.sample(solution.routes, n_routes_to_remove)
        return self.remove_route(solution, random_selection)

    def greedy_route_removal(self, solution, n_c = 0):
        """Removes the route with the least customer visits
        :param solution: solution before removal
        :param n_c: set to 0 by default because not relevant
        :return a set of removed customers"""
        def greedy_selection(solution, n_routes_to_remove):
            sorted_routes = sorted(solution.routes, key=lambda route: sum(self.data.type[visit.loc] == "c" for visit in route.visits))
            return sorted_routes[:n_routes_to_remove]

        return self.remove_route(solution, greedy_selection)

    # general methods
    def costs_removal(self, n_c, determinism_factor, solution, costs_func):
        """generalized function for worst-distance, worst-time, shaw removal and its variants
        :param n_c: number of customers to remove
        :param determinism_factor: a parameter that determines the likelihood of kth customer to be removed
        :param solution: solution before removal
        :param costs_func: the costs function to be considered
        :return a set of removed customers"""
        removal_costs = costs_func(solution)
        removal_costs.sort(key=lambda x: x[2], reverse=True)

        removed = []

        for i in range(n_c):
            removal_index = int(len(removal_costs) * (self.rnd.random() ** determinism_factor))
            to_remove = removal_costs.pop(removal_index)
            to_remove[0].remove_visit(to_remove[1])
            removed.append(to_remove[1].loc)

        return removed

    def shaw_costs_general(self, solution, shaw_param_1, shaw_param_2, shaw_param_3, shaw_param_4):
        """Calculates shaw removal costs
        :param: solution: solution before removal
        :param: shaw_param_1: shaw parameter 1
        :param: shaw_param_2: shaw parameter 2
        :param: shaw_param_3: shaw parameter 3
        :param: shaw_param_4: shaw parameter 4
        :return: a list of shaw removal costs for each location
        as a tuple of the route of the removal, the visit of the removal and the removal cost"""
        removal_costs = []
        rnd_route, rnd_visit = self.rnd.choice(solution.customer_visits)

        for route in solution.routes:
            for visit in route.visits:
                if self.data.type[visit.loc] != "c" or rnd_visit == visit:
                    continue

                costs_1 = shaw_param_1 * self.data.distance_matrix[rnd_visit.loc, visit.loc]
                costs_2 = shaw_param_2 * abs(self.data.ready_time[rnd_visit.loc] - self.data.ready_time[visit.loc])
                if rnd_route == route:
                    is_route_same = -1
                else:
                    is_route_same = 1
                costs_3 = shaw_param_3 * is_route_same
                costs_4 = shaw_param_4 * abs(self.data.demand[rnd_visit.loc] - self.data.demand[visit.loc])
                costs = costs_1 + costs_2 + costs_3 + costs_4
                removal_costs.append((route, visit, costs))

        return removal_costs

    def remove_route(self, solution, route_selection):
        """removes a random number of routes
        :param solution: solution before removal
        :param route_selection: RR operation to be used
        :return: a set of customers removed"""
        n_routes = len(solution.routes)
        routes_to_remove_min = max(1, int(0.1 * n_routes))
        routes_to_remove_max = max(1, int(0.3 * n_routes))
        n_routes_to_remove = self.rnd.randint(routes_to_remove_min, routes_to_remove_max)
        routes_to_remove = route_selection(solution, n_routes_to_remove)
        removed = []

        for route in routes_to_remove:
            removed_visits = solution.remove_route(route)

            for visit in removed_visits:
                if self.data.type[visit.loc] == "c":
                    removed.append(visit.loc)

        return removed

    def choose_route_removal(self):
        """chooses between random and greedy route removal according to their weights
        :return: a CR operation chosen"""
        RR_weights = [self.weights[self.operations[-2]], self.weights[self.operations[-1]]]
        return self.rnd.choices(self.operations[-2:], weights = RR_weights, k=1)[0]

    def get_n_to_remove(self):
        """randomly determines the number of customers to remove
        :return: the number of customers to remove"""
        n = self.data.n_customer
        LB = min(0.1 * n, 30)
        UB = min(0.4 * n, 60)
        return math.ceil(self.rnd.uniform(LB, UB))

    def choose_operation(self):
        """Randomly chooses a operation with probability reflected by the weights
        :return: the RR operation chosen"""
        return self.rnd.choices(self.operations, weights=list(self.weights.values()), k=1)[0]