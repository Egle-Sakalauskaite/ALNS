import math
import copy
from reader import Reader

def split_into_zones(data, solution):
    n_z = 25
    zones = {}
    x_min = min(data.x)
    x_max = max(data.x)
    y_min = min(data.y)
    y_max = max(data.y)
    dim = int(math.sqrt(n_z))
    zone_width = (x_max - x_min) / dim
    zone_height = (y_max - y_min) / dim

    for route_idx, route in enumerate(solution.routes):
        for idx, visit in enumerate(route.visits):
            if data.type[visit.loc] != "c":
                continue

            column_index = min(dim - 1, int((data.x[visit.loc] - x_min) / zone_width))
            row_index = min(dim - 1, int((data.y[visit.loc] - y_min) / zone_height))
            zone_index = row_index * dim + column_index
            if zone_index not in zones:
                zones[zone_index] = []
            zones[zone_index].append((route_idx, idx))

    return zones
def choose_operation(rnd, type):
    return rnd.choices(type.operations, type.weights, k=1)[0]

def increase_score(operations_used, score):
    for type, operation in operations_used:
        idx = type.operations.index(operation)
        type.times_used += 1
        type.scores[idx] += score

def update_weights(type):
    roulette_wheel_param = 0.25

    for i in range(len(type.operations)):
        type.weights[i] = type.weights[i] * (1 - roulette_wheel_param) + roulette_wheel_param*type.scores[i] / type.times_used[i]
        type.scores[i] = 0

def simulated_annealing(rnd, T, best, solution):
    if len(solution.routes) < len(best.routes):
        return True
    if len(solution.routes) == len(best.routes):
        if solution.total_distance < best.total_distance:
            return True

        delta = best.total_distance - solution.total_distance
        accept_prob = math.exp(-delta / T)

        return rnd.random() < accept_prob

def check_feasibility(data, solution):
    print()
    print()
    print(f"total distance: {solution.total_distance}")
    print(f"number of routes: {len(solution.routes)}")
    unvisited = set(data.type_range("c"))

    for i, route in enumerate(solution.routes):
        route.print()

        for visit in route.visits:
            if data.type[visit.loc] == "c":
                unvisited.remove(visit.loc)
            if visit.arrival_time > data.due_time[visit.loc]:
                raise ValueError("departure time violated")
            if visit.load_level_upon_departure < 0:
                raise ValueError("Load level violated")
            if not visit.is_battery_feasible:
                raise ValueError("battery violation")

    print(f"all customers visited? {len(unvisited) == 0}")
    print(f"unvisited: {unvisited}")
    if len(unvisited) > 0:
        raise ValueError(f"unvisited: {unvisited}")

    print()
    print()

