import helper
import copy
from route import Route
from stationInsertion import greedy_station_insertion

class CustomerInsertion:
    """Operations for inserting customers"""
    def __init__(self, data, rnd):
        self.data = data
        self.rnd = rnd
        self.operations = [self.greedy_insertion,
                           self.time_based_insertion,
                           self.zone_insertion,
                           self.regret_2_insertion,
                           self.regret_3_insertion]
        self.scores = {}
        self.weights = {}
        self.times_used = {}
        for operation in self.operations:
            self.scores[operation] = 0
            self.weights[operation] = 1 / len(self.operations)
            self.times_used[operation] = 0

    def customer_insertion(self, solution, removed):
        operation = self.choose_operation()

        while len(removed) > 0:
            inserted, solution = operation(solution, removed)
            if inserted is None:
                print(f"creating a new route!")
                new_route = Route(self.data)
                inserted = self.data.find_closest(0, removed)
                new_route.insert_at(inserted, 1)
                solution.add_route(new_route)

                while not new_route.is_battery_feasible:
                    to_insert = greedy_station_insertion(self.data, new_route)
                    if to_insert is None:
                        break
                    new_route.insert_at(*to_insert)


            print(f"inserted: {inserted}")
            removed.remove(inserted)

        return operation, solution


    # CI operations
    def greedy_insertion(self, solution, removed):
        """Inserts a removed  customer at a cheapest feasible position according to distance"""
        # print("CI: Greedy insertion")
        def costs_func(solution, removed):
            return self.insertion_costs(solution, removed, self.distance_costs)
        return self.insert_customer(solution, removed, costs_func)

    def time_based_insertion(self, solution, removed):
        """Inserts a removed  customer at a cheapest feasible position according to time"""
        # print("CI: Time based insertion")
        def costs_func(solution, removed):
            return self.insertion_costs(solution, removed, self.time_costs)
        return self.insert_customer(solution, removed, costs_func)

    def zone_insertion(self, solution, removed):
        """Same as time-based insertion, but only the routes that are in a random zone of the Cartesian plane are considered"""
        print("CI: Zone insertion")

        def costs_func(solution, removed):
            zones = helper.split_into_zones(self.data, solution)

            if len(zones.keys()) != 0:
                random_zone = self.rnd.choice(list(zones.keys()))
                routes_in_zone = set()
                for route, visit in zones[random_zone]:
                    routes_in_zone.add(solution.routes.index(route))

                return self.insertion_costs(solution, removed, self.time_costs, routes_in_zone)
            else:
                return self.insertion_costs(solution, removed, self.time_costs)

        return self.insert_customer(solution, removed, costs_func)

    def regret_2_insertion(self, solution, removed):
        """Customers are inserted according to how large the best and 2nd best insertion cost is"""
        # print("CI: Regret-2 insertion")
        return self.regret_k_insertion(2, solution, removed)

    def regret_3_insertion(self, solution, removed):
        """Customers are inserted according to how large the best and 3rd best insertion cost is"""
        # print("CI: Regret-3 insertion")
        return self.regret_k_insertion(3, solution, removed)


    # General methods
    def regret_k_insertion(self, k, solution, removed):
        """general function for regret-2 and regret-3 insertion"""
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

        return self.insert_customer(solution, removed, costs_func)

    def insert_customer(self, solution, removed, insertion_costs_func):
        """general function for inserting customers according to specific insertion costs criterion"""
        inserted = None
        insertion_costs = insertion_costs_func(solution, removed)

        for insertion in insertion_costs:
            route_idx, loc, idx, cost = insertion
            # print(f"inserting {loc} in ({route_idx, idx}) costs {cost}")
            copied_route = copy.deepcopy(solution.routes[route_idx])
            copied_route.insert_at(loc, idx)

            if copied_route.is_feasible:
                while not copied_route.is_battery_feasible:
                    to_insert = greedy_station_insertion(self.data, copied_route)
                    if to_insert is None:
                        break
                    copied_route.insert_at(*to_insert)

            if copied_route.is_feasible and copied_route.is_battery_feasible:
                solution.routes[route_idx] = copied_route
                inserted = loc
                break

        return inserted, solution

    def distance_costs(self, route, i, loc):
        """Returns a distance cost of inserting customer loc in a given route at position i"""
        pred = route.visits[i - 1].loc
        suc = route.visits[i].loc
        return self.data.distance_matrix[pred, loc] + self.data.distance_matrix[loc, suc]

    def time_costs(self, route, i, loc):
        """Returns a time cost of inserting customer loc in a given route at position i"""
        pred = route.visits[i - 1]
        suc = route.visits[i]
        current_start_time = min(suc.arrival_time, self.data.ready_time[suc.loc])
        travel_time = self.data.distance_matrix[pred.loc, loc] / self.data.velocity + self.data.distance_matrix[loc, suc.loc] / self.data.velocity
        new_arrival_time = pred.departure_time + travel_time + self.data.service_time[loc]
        new_start_time = min(new_arrival_time, self.data.ready_time[suc.loc])
        return new_start_time - current_start_time

    def insertion_costs(self, solution, removed, costs_func, routes_to_consider=None):
        """Returns all possible insertion costs of all removed customers according to specific cost function
        the costs are sorted in ascending order"""
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

    def choose_operation(self):
        """Randomly chooses an operation with probability reflected by the weights"""
        return self.rnd.choices(self.operations, weights=list(self.weights.values()), k=1)[0]
