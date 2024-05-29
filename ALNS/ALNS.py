import copy
import math
import helper

from customerInsertion import CustomerInsertion
from initialSolution import construct_initial_solution
from reader import Reader
import random
from customerRemoval import CustomerRemoval
from stationInsertion import StationInsertion
from stationRemoval import StationRemoval
from stationInsertion import greedy_station_insertion

# PARAMETERS
N_SR = 60
N_RR = 2000
n_RR = 1250
N_C = 200
N_S = 5500

sigma_1 = 25
sigma_2 = 20
sigma_3 = 21

temp_control_param = 0.4
cooling_rate = .9994
T = None

data = Reader("evrptw_instances//c101C5.xlsx")
n_c_LB = min(0.1*data.n_customer, 30)
n_c_UB = min(0.4*data.n_customer, 60)
n_s_LB = min(0.1*data.n_service, 30)
n_s_UB = min(0.4*data.n_service, 60)
seed = 42
rnd = random.Random()
rnd.seed(seed)
CR = CustomerRemoval(data, rnd)
CI = CustomerInsertion(data, rnd)
SR = StationRemoval(data, rnd)
SI = StationInsertion(data, rnd)

current_solution = construct_initial_solution(data)
removed_customers = []
best_solution = None
previous_solution = None
j = 1


while True:
    operations_used = []
    if j % N_SR == 0:
        # SR
        n_s = rnd.randint(n_s_LB, n_s_UB)
        operation = helper.choose_operation(rnd, SR)
        operation(n_s, current_solution)
        operations_used.append((SR, operation))
        # SI
        operation = helper.choose_operation(rnd, SI)
        current_solution = operation(current_solution)
        operations_used.append((SI, operation))
    elif j % N_RR == 0:
        for i in range(n_RR):
            # RR
            operation = CR.choose_route_removal()
            removed = operation(None, current_solution)
            operations_used.append(operation)
            removed_customers.extend(removed_customers)
            # CI
            if len(removed_customers) > 0:
                operation = helper.choose_operation(rnd, CI)
                operation(current_solution, removed)
                operations_used.append((CI, operation))
    else:
        # CR
        n_c = random.randint(n_c_LB, n_c_UB)
        operation = helper.choose_operation(rnd, CR)
        removed = operation(n_c, current_solution)
        operations_used.append((CR, operation))
        removed_customers.extend(removed_customers)
        # CI
        if len(removed_customers) > 0:
            operation = helper.choose_operation(rnd, CI)
            operation(current_solution, removed)
            operations_used.append((CI, operation))

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
                best_solution = current_solution
                score += sigma_1
            elif current_cost < previous_cost:
                score += sigma_2
            elif helper.simulated_annealing(rnd, T, best_solution, current_solution):
                score += sigma_3

        previous_solution = current_solution
        helper.increase_score(operations_used, score)

        j += 1
        if j % N_C == 0:
            # update CR and CI weights
            helper.update_weights(CR)
            helper.update_weights(CI)
        if j % N_S == 0:
            # update SR and SI weights
            helper.update_weights(SR)
            helper.update_weights(SI)

