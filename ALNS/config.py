# Set Ture if running a reduced number of iterations (2500), False if full run (25000)
PARTIAL_RUN = False

# Set True if full recharge or fixed partial recharging is used, False for free PR strategy
PR_FIXED = False
# Change PR strategy here
PR_STRATEGY = 0.4

# set True if solving the EVRPTW-BD (extension), False if solving EVRPTW (without battery degradation considered)
BATTERY_DEGRADATION = False
W_L_costs = [0.1, 0.5, 2.5]
W_H_costs = [0.2, 1, 5]
# change this accordingly
price_idx = 2

if BATTERY_DEGRADATION:
    lb = 0.25
    ub = 0.85
    W_L = W_L_costs[price_idx]
    W_H = W_H_costs[price_idx]
else:
    lb = 0
    ub = 1
    W_L = 0
    W_H = 0