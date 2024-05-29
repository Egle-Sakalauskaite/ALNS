from route import Route
import helper
import copy
import math

class StationInsertion:
    def __init__(self, data, rnd):
        self.data = data
        self.rnd = rnd
        self.operations = []
        self.times_used = []
        self.weights = [1 for _ in range(len(self.operations))]
        self.scores = {}

        for operation in self.operations:
            self.scores[operation] = 0

    def greedy_station_insertion(self, solution):
        for route in solution.routes:
            route = greedy_station_insertion(self.data, route)

        return solution

    def greedy_station_insertion_with_comparison(self, solution):
        for route in solution.routes:
            pass

def greedy_station_insertion(data, route):
    idx = route.first_battery_violation_idx
    inserted = False

    while not inserted and idx > 0:
        insertions = insertion_costs(data, route, idx)

        for insertion in insertions:
            loc, cost = insertion
            copied_route = copy.deepcopy(route)
            copied_route.insert_at(loc, idx)
            inserted_visit = copied_route.visits[idx]

            if inserted_visit.is_battery_feasible and copied_route.is_feasible:
                print("insertion is feasible")
                route = copied_route
                inserted = True
                break

        if not inserted:
            print(f"inserting at idx {idx} is infeasible")
            idx -= 1

    return route

def insertion_costs(data, route, idx):
    insertion_costs = []

    for loc in data.type_range("f"):
        pred = route.visits[idx - 1].loc
        suc = route.visits[idx].loc
        cost = data.distance_between(pred, loc) + data.distance_between(loc, suc)
        insertion_costs.append((loc, cost))

    insertion_costs.sort(key=lambda x: x[1], reverse=False)
    return insertion_costs
