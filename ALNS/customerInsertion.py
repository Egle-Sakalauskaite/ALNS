from collections import defaultdict
from stationInsertion import greedy_station_insertion
import helper
import copy

class CustomerInsertion:
    def __init__(self, data, rnd):
        self.data = data
        self.rnd = rnd
        self.operations = [self.greedy_insertion,
                           self.time_based_insertion,
                           self.zone_insertion,
                           self.regret_2_insertion,
                           self.regret_3_insertion]
        self.times_used = []
        self.weights = [1 for _ in range(len(self.operations))]
        self.scores = {}
        for operation in self.operations:
            self.scores[operation] = 0


    # CI operations
    def greedy_insertion(self, solution, removed):
        def costs_func(solution, removed):
            return self.insertion_costs(solution, removed, self.distance_costs)
        return self.customer_insertion(solution, removed, costs_func)

    def time_based_insertion(self, solution, removed):
        def costs_func(solution, removed):
            return self.insertion_costs(solution, removed, self.time_costs)
        return self.customer_insertion(solution, removed, costs_func)

    def zone_insertion(self, solution, removed):
        def costs_func(solution, removed):
            zones = helper.split_into_zones(self.data, solution)
            while True:
                random_zone = self.rnd.choice(list(zones.keys()))
                if len(zones[random_zone]) > 0:
                    break

            routes_in_zone = set()
            for route_idx, idx in zones[random_zone]:
                routes_in_zone.add(route_idx)

            print(f"routes in zone: {routes_in_zone}")
            return self.insertion_costs(solution, removed, self.time_costs, routes_in_zone)
        return self.customer_insertion(solution, removed, costs_func)

    def regret_2_insertion(self, solution, removed):
        return self.regret_k_insertion(2, solution, removed)

    def regret_3_insertion(self, solution, removed):
        return self.regret_k_insertion(3, solution, removed)


    # General methods
    def customer_insertion(self, solution, removed, insertion_costs_func):
        while len(removed) > 0:
            inserted = False
            insertion_costs = insertion_costs_func(solution, removed)
            for insertion in insertion_costs:
                route_idx, loc, idx, cost = insertion
                print(f"inserting {loc} in ({route_idx, idx}) costs {cost}")
                copied_solution = copy.deepcopy(solution)
                copied_solution.routes[route_idx].insert_at(loc, idx)

                if copied_solution.routes[route_idx].is_feasible:
                    print("insertion is feasible")
                    solution = copied_solution
                    removed.remove(loc)
                    inserted = True
                    break

            if not inserted:
                print("inserting remaining solutions is no longer feasible")
                break

        return solution
    def distance_costs(self, route, i, loc):
        pred = route.visits[i - 1].loc
        suc = route.visits[i].loc
        return self.data.distance_between(pred, loc) + self.data.distance_between(loc, suc)

    def time_costs(self, route, i, loc):
        pred = route.visits[i - 1]
        suc = route.visits[i]
        current_start_time = min(suc.arrival_time, self.data.ready_time[suc.loc])
        travel_time = self.data.distance_between(pred.loc, loc) / self.data.velocity + self.data.distance_between(loc, suc.loc) / self.data.velocity
        new_arrival_time = pred.departure_time + travel_time + self.data.service_time[loc]
        new_start_time = min(new_arrival_time, self.data.ready_time[suc.loc])
        return new_start_time - current_start_time

    def insertion_costs(self, solution, removed, costs_func, routes_to_consider=None):
        insertion_costs = []

        for loc in removed:
            for route_idx, route in enumerate(solution.routes):
                if routes_to_consider is not None:
                    if route_idx not in routes_to_consider:
                        continue

                for i in range(1, len(route.visits)):
                    cost = costs_func(route, i, loc)
                    insertion_costs.append((route_idx, loc, i, cost))

        insertion_costs.sort(key=lambda x: x[3], reverse=False)
        return insertion_costs

    def regret_k_insertion(self, k, solution, removed):
        def costs_func(solution, removed):
            regret_costs = []

            for loc in removed:
                insertion_costs = []
                for route_idx, route in enumerate(solution.routes):
                    for i in range(1, len(route.visits)):
                        cost = self.distance_costs(route, i, loc)
                        insertion_costs.append((route_idx, loc, i, cost))
                insertion_costs.sort(key=lambda x: x[3], reverse=False)

                for i in range(len(insertion_costs)):
                    route_idx, loc, i, cost = insertion_costs[i]

                    if i + k - 1 < len(insertion_costs):
                        cost -= insertion_costs[i + k - 1][3]

                    regret_costs.append((route_idx, loc, i, cost))

            regret_costs.sort(key=lambda x: x[3], reverse=True)
            return regret_costs

        return self.customer_insertion(solution, removed, costs_func)
