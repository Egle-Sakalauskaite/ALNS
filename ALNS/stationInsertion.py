import copy

class StationInsertion:
    """Operations for inserting stations"""
    def __init__(self, data, rnd):
        """initializes station insertion scores and weights at the beginning of the ALNS
        :param data: the instance data from the Reader
        :param rnd: the RND used for this instance run"""
        self.data = data
        self.rnd = rnd
        self.operations = [self.greedy_station_insertion,
                           self.greedy_station_insertion_with_comparison,
                           self.best_station_insertion]
        self.scores = {}
        self.weights = {}
        self.times_used = {}

        for operation in self.operations:
            self.scores[operation] = 0
            self.weights[operation] = 1 / len(self.operations)
            self.times_used[operation] = 0

    def station_insertion(self, solution):
        """Insert stations until battery feasibility is restored
        :param solution: the current solution
        :return: operation used and solution after insertion"""
        operation = self.choose_operation()

        while solution.is_feasible and not solution.is_battery_feasible:
            inserted_list, solution = operation(solution)
            if len(inserted_list) == 0:
                break

        return operation, solution

    def greedy_station_insertion(self, solution):
        """for each battery infeasible route, cheapest possible station inserted right before battery depletes below 0,
        or earlier if infeasible
        :param solution: the current solution
        :return the list of inserted stations and solution after insertion"""
        inserted_stations = []

        for route in solution.routes:
            to_insert = greedy_station_insertion(self.data, route)
            if to_insert is not None:
                route.insert_at(*to_insert)
                inserted_stations.append(to_insert[0])

        return inserted_stations, solution

    def greedy_station_insertion_with_comparison(self, solution):
        """same as greedy station insertion, but two positions before the first battery infeasible visit are considered
        cheapest of the two is inserted. If not feasible, greedy station insertion for earlier positions is performed
        :param solution: the current solution
        :return the list of inserted stations and solution after insertion"""
        inserted_stations = []

        for route in solution.routes:
            to_insert = greedy_station_insertion(self.data, route, True)
            if to_insert is not None:
                route.insert_at(*to_insert)
                inserted_stations.append(to_insert[0])

        return inserted_stations, solution

    def best_station_insertion(self, solution):
        """cheapest possible station insertion is performed in any position after last visit to the station
        :param solution: the current solution
        :return the list of inserted stations and solution after insertion"""
        inserted_stations = []

        for route in solution.routes:
            start_idx = route.first_battery_violation_idx
            all_insertions = []

            if start_idx < 1:
                continue

            last_station_visit = route.get_last_source_visit(start_idx)

            for i in range(last_station_visit + 1, start_idx):
                insertions = insertion_costs(self.data, route, i)
                all_insertions.extend(insertions)

            all_insertions.sort(key=lambda x: x[2], reverse=False)

            for insertion in all_insertions:
                loc, idx, cost = insertion
                copied_route = copy.deepcopy(route)
                copied_route.insert_at(loc, idx)
                inserted_visit = copied_route.visits[idx]

                if copied_route.required_charge < route.required_charge and inserted_visit.is_battery_feasible and copied_route.is_feasible:
                    route.insert_at(loc, idx)
                    inserted_stations.append(loc)
                    break

        return inserted_stations, solution

    def choose_operation(self):
        """Randomly chooses a operation with probability reflected by the weights
        :return operation chosen"""
        return self.rnd.choices(self.operations, weights=list(self.weights.values()), k=1)[0]

def greedy_station_insertion(data, route, with_comparison = False):
    """cheapest possible station inserted right before battery depletes below 0,or earlier if infeasible for specified route
    :param data: the data of the instance
    :param route: the route to be repaired
    :param with_comparison: tur, if greedy station insertion with comparison, false otherwise
    :return: the location and position indices of the station chosen to be inserted
    """
    start_idx = route.first_battery_violation_idx
    idx = start_idx
    to_insert = None

    while idx > 0 and to_insert is None:
        insertions = insertion_costs(data, route, idx)

        if with_comparison and idx == start_idx and idx > 1:
            insertions_earlier = insertion_costs(data, route, idx - 1)
            insertions.extend(insertions_earlier)
            insertions.sort(key=lambda x: x[2], reverse=False)

        for insertion in insertions:
            loc, i, cost = insertion
            copied_route = copy.deepcopy(route)
            copied_route.insert_at(loc, i)
            inserted_visit = copied_route.visits[i]

            if copied_route.required_charge < route.required_charge and inserted_visit.is_battery_feasible and copied_route.is_feasible:
                to_insert = (loc, i)
                break

        if to_insert is None:
            idx -= 1

    return to_insert

def insertion_costs(data, route, idx):
    """calculates insertion costs for all stations
    :param data: the data of the instance,
    :param route: the route to be repaired
    :param idx: the position index of insertion
    :return: the list of insertion costs"""
    insertion_costs = []

    for loc in data.type_range("f"):
        pred = route.visits[idx - 1].loc
        suc = route.visits[idx].loc
        cost = data.distance_matrix[pred, loc] + data.distance_matrix[loc, suc] - data.distance_matrix[pred, suc]
        insertion_costs.append((loc, idx, cost))

    insertion_costs.sort(key=lambda x: x[2], reverse=False)
    return insertion_costs
