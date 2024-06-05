from solution import Solution
from route import Route
import copy
from stationInsertion import greedy_station_insertion


def construct_initial_solution(data):
    """constructs a feasible initial solution"""
    solution = Solution(data)
    customers_to_serve = set(data.type_range("c"))
    # print("new route")
    feasible_route = Route(data)
    next_to_insert = data.find_closest(0, customers_to_serve)
    feasible_route.insert_at(next_to_insert, 1)
    # print(f"inserted: {next_to_insert}")
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
            # print(f"inserted: {best_to_insert}")
            current_customers_to_serve.remove(best_to_insert)
        else:
            # print("new route")
            solution.add_route(feasible_route)
            feasible_route = Route(data)
            next_to_insert = data.find_closest(0, customers_to_serve)
            # print(f"inserted: {next_to_insert}")
            customers_to_serve.remove(next_to_insert)
            feasible_route.insert_at(next_to_insert, 1)
            current_route = copy.deepcopy(feasible_route)
            current_customers_to_serve = copy.deepcopy(customers_to_serve)

        if not current_route.is_battery_feasible:
            # print("battery infeasible!")
            while current_route.is_feasible and not current_route.is_battery_feasible:
                to_insert = greedy_station_insertion(data, current_route)
                if to_insert is None:
                    break
                current_route.insert_at(*to_insert)
                # print(f"inserted: {to_insert[0]}")
            if not current_route.is_battery_feasible or not current_route.is_feasible:
                # print("backtracking...")
                solution.add_route(feasible_route)
                # print("new route")
                feasible_route = Route(data)
                next_to_insert = data.find_closest(0, customers_to_serve)
                # print(f"inserted: {next_to_insert}")
                customers_to_serve.remove(next_to_insert)
                feasible_route.insert_at(next_to_insert, 1)
                current_route = copy.deepcopy(feasible_route)
                current_customers_to_serve = copy.deepcopy(customers_to_serve)

                while current_route.is_feasible and not current_route.is_battery_feasible:
                    to_insert = greedy_station_insertion(data, current_route)
                    if to_insert is None:
                        break
                    current_route.insert_at(*to_insert)
                    print(f"inserted: {to_insert[0]}")

        feasible_route = current_route
        customers_to_serve = current_customers_to_serve

    solution.add_route(feasible_route)
    return solution


# testing...
# file_names = ["rc101_21", "rc201_21"]
#
# for file in file_names:
#     path = "evrptw_instances//" + file + ".xlsx"
#     data = Reader(path)
#     solution = construct_initial_solution(data)
#     helper.solution_to_JSON(solution, file + "_initial")

# data = Reader("evrptw_instances//c101_21.xlsx")
# # data = Reader("evrptw_instances//c101C5.xlsx")
# solution = construct_initial_solution(data)
# helper.check_feasibility(data, solution)
# seed = 42
# rnd = random.Random()
# rnd.seed(seed)
# CR = CustomerRemoval(data, rnd)
# CI = CustomerInsertion(data, rnd)
# SI = StationInsertion(data, rnd)
# SR = StationRemoval(data, rnd)
# operation_1, removed, solution = CR.customer_removal(solution)
# print(f"removed: {[i for i in removed]}")
# operation_2, solution = CI.customer_insertion(solution, removed)
# helper.check_feasibility(data, solution)
# operation_5, solution = SR.station_removal(solution)
# operation_6, solution = SI.station_insertion(solution)
# helper.check_feasibility(data, solution)
# for i in range(3):
#     operation_3, removed, solution = CR.route_removal(solution)
#     operation_4, solution = CI.customer_insertion(solution, removed)
# helper.check_feasibility(data, solution)
