import copy
import math
import time
import random

from reader import Reader
import helper
from initialSolution import construct_initial_solution
from customerInsertion import CustomerInsertion
from customerRemoval import CustomerRemoval
from stationInsertion import StationInsertion
from stationRemoval import StationRemoval
import tools
import config

# PARAMETERS
if config.PARTIAL_RUN:
    n_iter = 2500
    N_SR = 6
    N_RR = 200
    n_RR = 125
    N_C = 20
    N_S = 550
else:
    n_iter = 25000
    N_SR = 60
    N_RR = 2000
    n_RR = 1250
    N_C = 200
    N_S = 5500

sigma_1 = 25
sigma_2 = 20
sigma_3 = 21

temp_control_param = 0.4
cooling_rate = 0.9994


# All small-size instances
files = tools.get_small_instance_file_names()
seeds = [i for i in range(42, 78)]
instances = dict(zip(files, seeds))

# Large-size instances
# files = ["c101_21", "c201_21", "r101_21", "r201_21", "rc101_21", "rc201_21"]
# seeds = [i for i in range(78, 84)]
# instances = dict(zip(files, seeds))

# some of the small-size instances for EVRPTW-BD
# instances = {"c206C5": 48,
#              "r202C5": 60,
#              "rc204C5": 72,
#              "C101c10": 44,
#              "r201C10": 62,
#              "rc102C10": 68,
#              "c103C15": 46,
#              "r202C15": 64,
#              "rc202C15": 76}

for file, seed in instances.items():
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
    best_solution = previous_solution
    j = 1


    for k in range(n_iter):
        print(f"================== iteration {k} ===========================")
        current_solution = copy.deepcopy(previous_solution)
        operations_used = []
        # SR and SI
        if j % N_SR == 0:
            operation, current_solution = SR.station_removal(current_solution)
            operations_used.append((SR, operation))
            operation, current_solution = SI.station_insertion(current_solution)
            operations_used.append((SI, operation))
        # RR
        elif j % N_RR == 0:
            for i in range(n_RR):
                operation, removed, current_solution = CR.route_removal(current_solution)
                operations_used.append((CR, operation))
                operation, current_solution = CI.customer_insertion(current_solution, removed)
                operations_used.append((CI, operation))
        # CR and CI
        else:
            operation, removed, current_solution = CR.customer_removal(current_solution)
            operations_used.append((CR, operation))
            operation, current_solution = CI.customer_insertion(current_solution, removed)
            operations_used.append((CI, operation))

        # If a feasible solution was constructed, update the scores
        if current_solution.is_feasible and current_solution.is_battery_feasible:
            current_solution.remove_empty_routes()
            current_cost = current_solution.total_cost
            score = 0

            if T == None:
                T = temp_control_param * current_cost / math.log(2) / 100
            else:
                T *= cooling_rate

            best_cost = best_solution.total_cost
            previous_cost = previous_solution.total_cost

            if current_cost < best_cost:
                best_solution = current_solution
                score += sigma_1
            elif current_cost < previous_cost:
                score += sigma_2
            elif helper.simulated_annealing(rnd, T, best_solution, current_solution):
                score += sigma_3

            previous_solution = current_solution
            helper.increase_score(operations_used, score)

        j += 1

        # Updating weights
        if j % N_C == 0:
            CR = helper.update_weights(CR)
            CI = helper.update_weights(CI)
        if j % N_S == 0:
            SR = helper.update_weights(SR)
            SI = helper.update_weights(SI)

    end_time = time.time()
    elapsed_time = end_time - start_time

    helper.check_feasibility(data, best_solution)
    helper.solution_to_JSON(best_solution, file, elapsed_time)