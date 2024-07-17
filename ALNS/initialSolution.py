import copy
import config
# Importing appropriate Route class version according to the settings in config.py
if config.BATTERY_DEGRADATION:
    from routeBD import Route
elif config.PR_FIXED:
    from routeFixedPR import Route
else:
    from route import Route
from solution import Solution
from stationInsertion import greedy_station_insertion


def construct_initial_solution(data):
    """constructs a feasible initial solution
    :param data: the instance data as a Reader object
    :return: the constructed feasible solution"""
    solution = Solution(data)
    customers_to_serve = set(data.type_range("c"))
    feasible_route = Route(data)
    next_to_insert = data.find_closest(0, customers_to_serve)
    feasible_route.insert_at(next_to_insert, 1)
    customers_to_serve.remove(next_to_insert)

    while len(customers_to_serve) > 0:
        current_route = copy.deepcopy(feasible_route)
        current_customers_to_serve = copy.deepcopy(customers_to_serve)
        best_insertion = None
        best_to_insert = None
        best_distance = 99999999999

        for i in range(len(current_route.visits) - 1):
            for customer in current_customers_to_serve:
                copied_route = copy.deepcopy(current_route)
                copied_route.insert_at(customer, i+1)

                if copied_route.is_feasible and copied_route.distance < best_distance:
                    best_insertion = copied_route
                    best_to_insert = customer
                    best_distance = copied_route.distance

        if best_insertion is not None:
            current_route = best_insertion
            current_customers_to_serve.remove(best_to_insert)
        else:
            solution.add_route(feasible_route)
            feasible_route = Route(data)
            next_to_insert = data.find_closest(0, customers_to_serve)
            customers_to_serve.remove(next_to_insert)
            feasible_route.insert_at(next_to_insert, 1)
            current_route = copy.deepcopy(feasible_route)
            current_customers_to_serve = copy.deepcopy(customers_to_serve)

        if not current_route.is_battery_feasible:
            while current_route.is_feasible and not current_route.is_battery_feasible:
                to_insert = greedy_station_insertion(data, current_route)
                if to_insert is None:
                    break
                current_route.insert_at(*to_insert)
            if not current_route.is_battery_feasible or not current_route.is_feasible:
                solution.add_route(feasible_route)
                feasible_route = Route(data)
                next_to_insert = data.find_closest(0, customers_to_serve)
                customers_to_serve.remove(next_to_insert)
                feasible_route.insert_at(next_to_insert, 1)
                current_route = copy.deepcopy(feasible_route)
                current_customers_to_serve = copy.deepcopy(customers_to_serve)

                while current_route.is_feasible and not current_route.is_battery_feasible:
                    to_insert = greedy_station_insertion(data, current_route)
                    if to_insert is None:
                        break
                    current_route.insert_at(*to_insert)

        feasible_route = current_route
        customers_to_serve = current_customers_to_serve

    solution.add_route(feasible_route)
    return solution
