import copy
import config
import helper
from stationInsertion import greedy_station_insertion
# Importing appropriate Route class version according to the settings in config.py
if config.BATTERY_DEGRADATION:
    from routeBD import Route
elif config.PR_FIXED:
    from routeFixedPR import Route
else:
    from route import Route


class CustomerInsertion:
    """Operations for inserting customers"""
    def __init__(self, data, rnd):
        """initializes customer insertion scores and weights at the beginning of the ALNS
        :param data: the instance data from the Reader
        :param rnd: the RND used for this instance run"""
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

        # All scores are initially set to 0 and the weights are equal
        for operation in self.operations:
            self.scores[operation] = 0
            self.weights[operation] = 1 / len(self.operations)
            self.times_used[operation] = 0

    def customer_insertion(self, solution, removed):
        """performs customer insertion on the solution by performing one of the CI operations
         until all customers in the removed list are inserted
        :param solution: the current solution
        :param removed: a set of customers to be inserted
        :return: the operation that was used and the solution after all insertions"""
        operation = self.choose_operation()

        while len(removed) > 0:
            inserted, solution = operation(solution, removed)
            if inserted is None:
                # No feasible insertion found, starting a new route...
                new_route = Route(self.data)
                inserted = self.data.find_closest(0, removed)
                new_route.insert_at(inserted, 1)
                solution.add_route(new_route)

                # Making new route battery feasible
                while not new_route.is_battery_feasible:
                    to_insert = greedy_station_insertion(self.data, new_route)
                    if to_insert is None:
                        break
                    new_route.insert_at(*to_insert)

            removed.remove(inserted)

        return operation, solution

    # CI operations
    def greedy_insertion(self, solution, removed):
        """Inserts a removed  customer at a cheapest feasible position according to distance
        :param solution: the current solution
        :param removed: a set of customers to be inserted
        :return: location index of the customer that was inserted  and the solution after the insertion
        or None and solution as it was if no insertion is feasible in the currently existing routes"""
        def costs_func(solution, removed):
            return self.insertion_costs(solution, removed, self.distance_costs)
        return self.insert_customer(solution, removed, costs_func)

    def time_based_insertion(self, solution, removed):
        """Inserts a removed  customer at a cheapest feasible position according to time
        :param solution: the current solution
        :param removed: a set of customers to be inserted
        :return: location index of the customer that was inserted  and the solution after the insertion
        or None and solution as it was if no insertion is feasible in the currently existing routes"""
        def costs_func(solution, removed):
            return self.insertion_costs(solution, removed, self.time_costs)
        return self.insert_customer(solution, removed, costs_func)

    def zone_insertion(self, solution, removed):
        """Same as time-based insertion, but only the routes that are in a random zone of the Cartesian plane are considered
        :param solution: the current solution
        :param removed: a set of customers to be inserted
        :return: location index of the customer that was inserted  and the solution after the insertion
        or None and solution as it was if no insertion is feasible in the currently existing routes"""
        def costs_func(solution, removed):
            zones = helper.split_into_zones(self.data, solution)

            # If current solution has at least one zone
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
        """Customers are inserted according to how large the best and 2nd best insertion cost is
        :param solution: the current solution
        :param removed: a set of customers to be inserted
        :return: location index of the customer that was inserted  and the solution after the insertion
        or None and solution as it was if no insertion is feasible in the currently existing routes"""
        return self.regret_k_insertion(2, solution, removed)

    def regret_3_insertion(self, solution, removed):
        """Customers are inserted according to how large the best and 3rd best insertion cost is
        :param solution: the current solution
        :param removed: a set of customers to be inserted
        :return: location index of the customer that was inserted  and the solution after the insertion
        or None and solution as it was if no insertion is feasible in the currently existing routes"""
        return self.regret_k_insertion(3, solution, removed)


    # General methods
    def regret_k_insertion(self, k, solution, removed):
        """general function for regret-2 and regret-3 insertion
        :param k: 2 if regret-2 is performed, 3 if regret-3
        :param solution: the current solution
        :param removed: a set of customers to be inserted
        :return: location index of the customer that was inserted  and the solution after the insertion
        or None and solution as it was if no insertion is feasible in the currently existing routes"""
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
        """general function for inserting customers according to specific insertion costs criterion
        :param solution: the current solution
        :param removed: a set of customers to be inserted
        :param insertion_costs_func: a function of constructing the list for insertion costs
        :return: location index of the customer that was inserted  and the solution after the insertion
        or None and solution as it was if no insertion is feasible in the currently existing routes"""
        inserted = None
        insertion_costs = insertion_costs_func(solution, removed)

        for insertion in insertion_costs:
            route_idx, loc, idx, cost = insertion
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
        """Returns a distance cost of inserting customer loc in a given route at position i
        :param: route: route of the insertion
        :param: i: route position index of the location that would be inserted
        :param: loc: location index of the location that would be inserted
        :return the change in distance after the insertion"""
        pred = route.visits[i - 1].loc
        suc = route.visits[i].loc
        return self.data.distance_matrix[pred, loc] + self.data.distance_matrix[loc, suc] - self.data.distance_matrix[pred, suc]

    def time_costs(self, route, i, loc):
        """Returns a time cost of inserting customer loc in a given route at position i
        :param: route: route of the insertion
        :param: i: route position index of the location that would be inserted
        :param: loc: location index of the location that would be inserted
        :return the change in travel time after the insertion"""
        pred = route.visits[i - 1]
        suc = route.visits[i]
        current_start_time = min(suc.arrival_time, self.data.ready_time[suc.loc])
        travel_time = self.data.distance_matrix[pred.loc, loc] / self.data.velocity + self.data.distance_matrix[loc, suc.loc] / self.data.velocity
        new_arrival_time = pred.departure_time + travel_time + self.data.service_time[loc]
        new_start_time = min(new_arrival_time, self.data.ready_time[suc.loc])
        return new_start_time - current_start_time

    def insertion_costs(self, solution, removed, costs_func, routes_to_consider=None):
        """Returns all possible insertion costs of all removed customers according to specific cost function
        the costs are sorted in ascending order
        :param solution: the current solution
        :param removed: a set of customers that need to be inserted
        :param costs_func: the function according to which insertion costs must be calculated
        :param routes_to_consider: a set of routes available for insertion
        or None if all routes can be considered
        :return: a list of sorted insertion costs as tuples:
        (route idx of insertion, location idx of insertion, position in the route idx of insertion, the cost of insertion)"""
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
        """Randomly chooses an operation with probability reflected by the weights
        :return: the CI operation chosen"""
        return self.rnd.choices(self.operations, weights=list(self.weights.values()), k=1)[0]
