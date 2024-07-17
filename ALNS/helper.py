import math
import json
import numpy as np
import config


def split_into_zones(data, solution):
    """splits the customers in solution into zones according to the location in the Cartesian plane
    :param data: data object of the current instance
    :param solution: solution to split into zones
    :return: a dictionary of zones, where the key is a zone index and the value is a list of visits in each zone"""
    n_z = 25
    zones = {}
    x_min = min(data.x)
    x_max = max(data.x)
    y_min = min(data.y)
    y_max = max(data.y)
    dim = int(math.sqrt(n_z))
    zone_width = (x_max - x_min) / dim
    zone_height = (y_max - y_min) / dim

    for route in solution.routes:
        for visit in route.visits:
            if data.type[visit.loc] != "c":
                continue

            column_index = min(dim - 1, int((data.x[visit.loc] - x_min) / zone_width))
            row_index = min(dim - 1, int((data.y[visit.loc] - y_min) / zone_height))
            zone_index = row_index * dim + column_index
            if zone_index not in zones:
                zones[zone_index] = []
            zones[zone_index].append((route, visit))

    return zones

def simulated_annealing(rnd, T, best, solution):
    """returns true if a solution is accepted according to simulated annealing
    :param rnd: random number generator
    :param T: current temperature parameter
    :param best: the best solution dus far
    :param solution: solution to accept/reject
    :return true, if the solution was accepted, false otherwise"""
    if len(solution.routes) < len(best.routes):
        return True
    if len(solution.routes) == len(best.routes):
        if solution.total_cost < best.total_cost:
            return True

        delta = best.total_cost - solution.total_cost
        accept_prob = np.exp(-delta / T)

        return rnd.random() < accept_prob

def increase_score(operations_used, score):
    """increases the score for each operation in the list
    :param operations_used: the list of operations used expressed as tuples,
    where first element is the type of operation (CR, SI ect) and second is the operation itself
    :param score: the score obtained by the solution"""
    for type, operation in operations_used:
        type.times_used[operation] += 1
        type.scores[operation] += score

def update_weights(type):
    """updates the weights of operations of specified type according to the current score
    resets the score to 0 after
    :param type: the type of operations to update (CR, SI ect)
    :return the updated version of CR, CI, SR or SI"""
    roulette_wheel_param = 0.25

    for opr in type.operations:
        if type.times_used[opr] > 0:
            type.weights[opr] = type.weights[opr] * (1 - roulette_wheel_param) + roulette_wheel_param*type.scores[opr] / type.times_used[opr]
            type.scores[opr] = 0
            type.times_used[opr] = 0

    return type

def check_feasibility(data, solution):
    """Prints the solution and checks if solution is feasible
    if not feasible, Value errors are thrown
    :param data: data object of the current instance
    :param solution: solution to check"""
    print()
    print()
    print(f"total distance: {solution.total_distance}")
    print(f"total battery degradation cost: {solution.total_battery_degradation_cost}")
    print(f"number of routes: {len(solution.routes)}")
    print(f"is solution feasible?: {solution.is_feasible}")
    print(f"is solution battery feasible? {solution.is_battery_feasible}")
    unvisited = set(data.type_range("c"))

    for i, route in enumerate(solution.routes):
        route.print()

        for visit in route.visits:
            if data.type[visit.loc] == "c":
                unvisited.remove(visit.loc)
            if visit.arrival_time > data.due_time[visit.loc]:
                raise ValueError("Due time violated")
            if visit.load_level_upon_departure < 0:
                raise ValueError("Load level violated")
            if not visit.is_battery_feasible:
                raise ValueError("Battery violation")

    if len(unvisited) > 0:
        raise ValueError(f"unvisited: {unvisited}")

    print()
    print()

def solution_to_JSON(solution, filename, time = 0.0):
    """saves the solution to a json file
    :param solution: solution object to save to json
    :param filename: file name to save to
    :param time: runtime of obtaining the solution"""
    if config.BATTERY_DEGRADATION:
        file_path = "extension_solutions//" + filename + "_" + str(config.W_H) + ".json"
    else:
        file_path = "json_solutions//" + filename + "_PR" + str(config.PR_STRATEGY) + ".json"
    solution_dict = {}
    solution_dict["Total distance:"] = solution.total_distance
    solution_dict["Total battery degradation cost:"] = solution.total_battery_degradation_cost
    solution_dict["Feasible?"] = solution.is_feasible
    solution_dict["Battery feasible?"] = solution.is_battery_feasible
    solution_dict["All customers visited?"] = solution.all_customers_visited
    solution_dict["Time to obtain:"] = time
    solution_dict["Routes:"] = []
    for route in solution.routes:
        route_dict = {}
        route_dict["Distance:"] = route.distance
        route_dict["Feasible"] = route.is_feasible
        route_dict["Battery feasible?"] = route.is_battery_feasible
        route_dict["Visits:"] = []
        for visit in route.visits:
            visit_dict = {}
            visit_dict["Location:"] = visit.loc
            visit_dict["Arrival time:"] = visit.arrival_time
            visit_dict["Charged quantity:"] = visit.charge_quantity
            route_dict["Visits:"].append(visit_dict)
        solution_dict["Routes:"].append(route_dict)
    with open(file_path, 'w') as json_file:
        json.dump(solution_dict, json_file, indent=4)


