import math
from solution import Solution
from route import Route
from reader import Reader
import helper
import copy
import random
from stationInsertion import greedy_station_insertion
from customerRemoval import CustomerRemoval
from customerInsertion import CustomerInsertion

def construct_initial_solution(data):
    solution = Solution(data)
    customers_to_serve = set(data.type_range("c"))
    print("new route")
    feasible_route = Route(data)
    next_to_insert = data.find_closest(0, customers_to_serve)
    feasible_route.insert_at(next_to_insert, 1)
    print(f"inserted: {next_to_insert}")
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
            print(f"inserted: {best_to_insert}")
            current_customers_to_serve.remove(best_to_insert)
        else:
            print("new route")
            solution.add_route(feasible_route)
            feasible_route = Route(data)
            next_to_insert = data.find_closest(0, customers_to_serve)
            print(f"inserted: {next_to_insert}")
            customers_to_serve.remove(next_to_insert)
            feasible_route.insert_at(next_to_insert, 1)
            current_route = copy.deepcopy(feasible_route)
            current_customers_to_serve = copy.deepcopy(customers_to_serve)

        if not current_route.is_battery_feasible:
            print("battery infeasible!")
            current_route = copy.deepcopy(current_route)
            current_route = greedy_station_insertion(data, current_route)
            if not current_route.is_battery_feasible or not current_route.is_feasible:
                print("backtracking...")
                solution.add_route(feasible_route)
                print("new route")
                feasible_route = Route(data)
                next_to_insert = data.find_closest(0, customers_to_serve)
                print(f"inserted: {next_to_insert}")
                customers_to_serve.remove(next_to_insert)
                feasible_route.insert_at(next_to_insert, 1)
                current_route = copy.deepcopy(feasible_route)
                current_customers_to_serve = copy.deepcopy(customers_to_serve)

                if not current_route.is_battery_feasible:
                    current_route = greedy_station_insertion(data, current_route)

        feasible_route = current_route
        customers_to_serve = current_customers_to_serve

    solution.add_route(feasible_route)
    return solution


# testing...
data = Reader("evrptw_instances//c101_21.xlsx")
# data = Reader("evrptw_instances//c101C5.xlsx")
solution = construct_initial_solution(data)
helper.check_feasibility(data, solution)
seed = 40
rnd = random.Random()
rnd.seed(seed)
CR = CustomerRemoval(data, rnd)
CI = CustomerInsertion(data, rnd)

removed = CR.random_removal(15, solution)
print(f"removed: {[i for i in removed]}")
solution = CI.greedy_insertion(solution, removed)
helper.check_feasibility(data, solution)
