import copy
import math
import helper
import time

from customerInsertion import CustomerInsertion
from initialSolution import construct_initial_solution
from reader import Reader
import random
from customerRemoval import CustomerRemoval
from stationInsertion import StationInsertion
from stationRemoval import StationRemoval

# PARAMETERS
n_iter = 2500

N_SR = 6
N_RR = 200
n_RR = 125
N_C = 20
N_S = 550

sigma_1 = 25
sigma_2 = 20
sigma_3 = 21

temp_control_param = 0.4
cooling_rate = 0.9994
seed = 42
files = helper.get_small_instance_file_names()

for file in files:
    start_time = time.time()
    T = None
    path = "evrptw_instances//" + file + ".xlsx"
    data = Reader(path)
    rnd = random.Random()
    rnd.seed(seed)

    CR = CustomerRemoval(data, rnd)
    CI = CustomerInsertion(data, rnd)
    SR = StationRemoval(data, rnd)
    SI = StationInsertion(data, rnd)

    previous_solution = construct_initial_solution(data)
    best_solution = None
    j = 1


    for k in range(n_iter):
        print(f"================== iteration {k} ===========================")
        current_solution = copy.deepcopy(previous_solution)
        helper.check_feasibility(data, current_solution)
        operations_used = []
        if j % N_SR == 0:
            print("Station Removal")
            operation, current_solution = SR.station_removal(current_solution)
            operations_used.append((SR, operation))
            print("Station Insertion")
            operation, current_solution = SI.station_insertion(current_solution)
            operations_used.append((SI, operation))
        elif j % N_RR == 0:
            for i in range(n_RR):
                print("Route Removal")
                operation, removed, current_solution = CR.route_removal(current_solution)
                operations_used.append((CR, operation))
                print("Customer Insertion")
                operation, current_solution = CI.customer_insertion(current_solution, removed)
                operations_used.append((CI, operation))
        else:
            print("Customer Removal")
            operation, removed, current_solution = CR.customer_removal(current_solution)
            print(f"removed: {removed}")
            operations_used.append((CR, operation))
            print("Customer Insertion")
            operation, current_solution = CI.customer_insertion(current_solution, removed)
            operations_used.append((CI, operation))

        if current_solution.is_feasible and current_solution.is_battery_feasible:
            current_solution.remove_empty_routes()
            # helper.check_feasibility(data, current_solution)
            print("solution is feasible!")
            current_cost = current_solution.total_distance
            score = 0

            if T == None:
                T = temp_control_param * current_cost / math.log(2) / 100
                best_solution = current_solution
            else:
                T *= cooling_rate

                best_cost = best_solution.total_distance
                previous_cost = previous_solution.total_distance

                if current_cost < best_cost:
                    print("new best solution found")
                    best_solution = current_solution
                    score += sigma_1
                elif current_cost < previous_cost:
                    print("solution was improved")
                    score += sigma_2
                elif helper.simulated_annealing(rnd, T, best_solution, current_solution):
                    print("solution was accepted according to SA")
                    score += sigma_3

            previous_solution = current_solution
            helper.increase_score(operations_used, score)

        j += 1

        if j % N_C == 0:
            print("updating CR and CI weights")
            helper.update_weights(CR)
            helper.update_weights(CI)
        if j % N_S == 0:
            print("updating SR and SI weights")
            helper.update_weights(SR)
            helper.update_weights(SI)

    end_time = time.time()
    elapsed_time = end_time - start_time

    helper.check_feasibility(data, best_solution)
    helper.solution_to_JSON(best_solution, file, elapsed_time)
    seed += 1

