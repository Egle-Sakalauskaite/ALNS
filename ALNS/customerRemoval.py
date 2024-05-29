import math
import helper

class CustomerRemoval:
    def __init__(self, data, rnd):
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
        self.times_used = []
        self.weights = [1  for _ in range(len(self.operations))]
        self.scores = {}
        for operation in self.operations:
            self.scores[operation] = 0

    # CR operations
    def random_removal(self, n_c, solution):
        removed = []

        for i in range(n_c):
            selected_route, selected_visit = self.rnd.choice(solution.customer_visits)
            selected_route.remove_visit(selected_visit)
            removed.append(selected_visit.loc)

        return removed

    def worst_distance_removal(self, n_c, solution):
        def distance_costs(solution):
            removal_costs = []

            for route in solution.routes:
                for i, visit in enumerate(route.visits):
                    if self.data.type[visit.loc] != "c":
                        continue

                    pred = route.visits[i - 1].loc
                    suc = route.visits[i + 1].loc
                    costs = self.data.distance_between(visit.loc, pred) + self.data.distance_between(visit.loc, suc)
                    removal_costs.append((route, visit, costs))

            return removal_costs

        return self.costs_removal(n_c, 4, solution, distance_costs)

    def worst_time_removal(self, n_c, solution):
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

    def shaw_removal(self, n_c, solution):
        def shaw_costs(solution):
            return self.shaw_costs_general(solution, 0.5, 13, 0.15, 0.25)

        return self.costs_removal(n_c, 12, solution, shaw_costs)

    def proximity_based_removal(self, n_c, solution):
        def proximity_based_costs(solution):
            return self.shaw_costs_general(solution, 1, 0, 0, 0)

        return self.costs_removal(n_c, 12, solution, proximity_based_costs)

    def time_based_removal(self, n_c, solution):
        def time_based_costs(solution):
            return self.shaw_costs_general(solution, 0, 1, 0, 0)

        return self.costs_removal(n_c, 12, solution, time_based_costs)

    def demand_based_removal(self, n_c, solution):
        def demand_based_costs(solution):
            return self.shaw_costs_general(solution, 0, 0, 0, 1)

        return self.costs_removal(n_c, 12, solution, demand_based_costs)

    def zone_removal(self, n_c, solution):
        removed = []
        zones = helper.split_into_zones(self.data, solution)

        while True:
            zone_to_remove = self.rnd.choice(list(zones.keys()))

            if len(zones[zone_to_remove]) > 0:
                break

        for route_idx, idx in zones[zone_to_remove]:
            route = solution.routes[route_idx]
            to_remove = route.visits[idx]
            route.remove_visit(to_remove)
            removed.append(to_remove.loc)

        return removed

    def random_route_removal(self, n_c, solution):
        def random_selection(solution, n_routes_to_remove):
            return self.rnd.sample(solution.routes, n_routes_to_remove)
        return self.route_removal(solution, random_selection)

    def greedy_route_removal(self, n_c, solution):
        def greedy_selection(solution, n_routes_to_remove):
            sorted_routes = sorted(solution.routes, key=lambda route: sum(self.data.type[visit.loc] == "c" for visit in route.visits))
            return sorted_routes[:n_routes_to_remove]

        return self.route_removal(solution, greedy_selection)

    # general methods
    def costs_removal(self, n_c, determinism_factor, solution, costs_func):
        removal_costs = costs_func(solution)
        removal_costs.sort(key=lambda x: x[2], reverse=True)

        # print("removal costs:")
        # for route, visit, costs in removal_costs:
        #     print(f"{visit.loc}: {costs}")

        removed = []

        for i in range(n_c):
            removal_index = int(len(removal_costs) * (self.rnd.random() ** determinism_factor))
            to_remove = removal_costs.pop(removal_index)
            to_remove[0].remove_visit(to_remove[1])
            removed.append(to_remove[1].loc)

        return removed

    def shaw_costs_general(self, solution, shaw_param_1, shaw_param_2, shaw_param_3, shaw_param_4):
        removal_costs = []
        rnd_route, rnd_visit = self.rnd.choice(solution.customer_visits)
        print(f"benchmark: {rnd_visit.loc}")

        for route in solution.routes:
            for visit in route.visits:
                if self.data.type[visit.loc] != "c" or rnd_visit == visit:
                    continue

                costs_1 = shaw_param_1 * self.data.distance_between(rnd_visit.loc, visit.loc)
                costs_2 = shaw_param_2 * abs(self.data.ready_time[rnd_visit.loc] - self.data.ready_time[visit.loc])
                if rnd_route == route:
                    is_route_same = -1
                else:
                    is_route_same = 1
                costs_3 = shaw_param_3 * is_route_same
                costs_4 = shaw_param_4 * abs(self.data.demand[rnd_visit.loc] - self.data.demand[visit.loc])
                costs = costs_1 + costs_2 + costs_3 + costs_4
                print(f"costs between {rnd_visit.loc} and {visit.loc}: {costs_1} + {costs_2} + {costs_3} + {costs_4}")
                removal_costs.append((route, visit, costs))

        return removal_costs

    def route_removal(self, solution, route_selection):
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
        return self.rnd.choices(self.operations[-2:], self.weights[-2:], k=1)[0]
