import json
import math
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from reader import Reader


def excel_to_csv(excel_file):
    """Writes the excel file sheets into separate csv files
    :param excel_file: the name of the excel file"""
    excel_path = f"evrptw_instances//{excel_file}.xlsx"

    locations = pd.read_excel(excel_path, sheet_name="locations")
    other = pd.read_excel(excel_path, sheet_name="other")

    csv_path = f"evrptw_instances//{excel_file}_locations.csv"
    locations.to_csv(csv_path, index=False)

    csv_path = f"evrptw_instances//{excel_file}_other.csv"
    other.to_csv(csv_path, index=False)

def get_small_instance_file_names():
    """Returns a list of file names for all small instances
    :return: a list of file names"""
    files = []

    files_c1 = ["c101C5", "c103C5", "c101C10", "c104C10", "c103C15", "c106C15"]
    files_c2 = ["c206C5", "c208C5", "c202C10", "c205C10", "c202C15", "c208C15"]
    files_r1 = ["r104C5", "r105C5", "r102C10", "r103C10", "r102C15", "r105C15"]
    files_r2 = ["r202C5", "r203C5", "r201C10", "r203C10", "r202C15", "r209C15"]
    files_rc1 = ["rc105C5", "rc108C5", "rc102C10", "rc108C10", "rc103C15", "rc108C15"]
    files_rc2 = ["rc204C5", "rc208C5", "rc201C10", "rc205C10", "rc202C15", "rc204C15"]
    files.extend(files_c1)
    files.extend(files_c2)
    files.extend(files_r1)
    files.extend(files_r2)
    files.extend(files_rc1)
    files.extend(files_rc2)
    return files

def convert_MILP_solution_to_JSON(filename, W_H = ""):
    """Converts the MILP solution from an excel file to a json file.
    Only decision variables unequal to 0 were saved in the excel file.
    The indexing is reverted to the order before dummies were added.
    :param: filename: the name of the instance
    :param: W_H: the W_H cost as a string to differentiate between files
    when considering battery degradation"""
    reader = Reader("evrptw_instances//" + filename + ".xlsx")
    n_service = reader.n_service
    n_customer = reader.n_customer
    n_dummy = n_service ** 2
    delta = n_dummy - n_service
    N = n_dummy + n_customer
    dist_mat = reader.distance_matrix

    # dict reconverts the indexing from the one that includes dummies to original order
    dict = {}
    dict[0] = 0

    for i in range(1, n_dummy + 1):
        dict[i] = (i + n_service - 1) // n_service
    for i in range(n_dummy + 1, N + 1):
        dict[i] = i - delta

    dict[N + 1] = 0
    arcs = []
    load = np.zeros(N+2)
    arrival = np.zeros(N+2)
    battery_upon_arrival = np.zeros(N+2)
    battery_upon_departure = np.zeros(N+2)

    path = "MILP_solutions//" + filename
    df = pd.read_csv(path + ".csv", header=None, names=range(4))
    path_soc = "MILP_output//" + filename + "_" + str(W_H)
    df_soc = pd.read_csv(path_soc + ".csv", header=None, names=range(4))
    objective = df.iloc[0, 1]
    runtime = int(df.iloc[1, 1]) / 1000
    distance = 0

    for i in range(2, len(df)):
        var_type = df.iloc[i, 0]
        if var_type == "x" and not math.isclose(df.iloc[i, 3], 0, abs_tol=1e-5):
            i_loc = int(df.iloc[i, 1])
            j_loc = int(df.iloc[i, 2])
            arcs.append((i_loc, j_loc))
            distance += dist_mat[dict[i_loc], dict[j_loc]]
        else:
            loc = int(df.iloc[i, 1])
            val = float(df.iloc[i, 2])
            if var_type == "u":
                load[loc] = val
            elif var_type == "tau":
                arrival[loc] = val

    for i in range(2, len(df_soc)):
        var_type = df_soc.iloc[i, 0]
        loc = int(df_soc.iloc[i, 1])
        val = float(df_soc.iloc[i, 2])
        if var_type == "y":
            battery_upon_arrival[loc] = val
        elif var_type == "Y":
            battery_upon_departure[loc] = val

    arcs.sort(key=lambda x: x[0], reverse=False)
    solution = {}
    solution["Objective:"] = objective
    solution["Distance:"] = distance
    solution["Time to obtain:"] = runtime
    solution["Routes:"] = []
    current_idx = 0

    while arcs[current_idx][0] == 0:
        route_dict = {"Visits:": []}
        from_depot = {}
        from_depot["Location:"] = 0
        from_depot["Arrival:"] = arrival[0]
        from_depot["Load upon arrival:"] = load[0]
        from_depot["Battery upon arrival:"] = battery_upon_arrival[0]
        from_depot["Battery upon departure:"] = battery_upon_departure[0]
        route_dict["Visits:"].append(from_depot)
        current = arcs[current_idx][1]
        while current != N + 1:
            loc = current
            # if same station visited in a row, merge the visits
            if route_dict["Visits:"][-1]["Location:"] == dict[loc]:
                route_dict["Visits:"][-1]["Battery upon departure:"] = battery_upon_departure[loc]
            else:
                visit = {}
                visit["Location:"] = dict[loc]
                visit["Arrival:"] = arrival[loc]
                visit["Load upon arrival:"] = load[loc]
                visit["Battery upon arrival:"] = battery_upon_arrival[loc]
                if loc == 0 or reader.type[dict[loc]] == "f":
                    visit["Battery upon departure:"] = battery_upon_departure[loc]
                else:
                    visit["Battery upon departure:"] = battery_upon_arrival[loc]

                route_dict["Visits:"].append(visit)

            for arc in arcs:
                if arc[0] == current:
                    current = arc[1]
                    break

        to_depot = {}
        to_depot["Location:"] = 0
        to_depot["Arrival:"] = arrival[N + 1]
        to_depot["Load upon arrival:"] = load[N + 1]
        to_depot["Battery upon arrival:"] = battery_upon_arrival[N + 1]
        to_depot["Battery upon departure:"] = battery_upon_departure[N + 1]
        route_dict["Visits:"].append(to_depot)
        solution["Routes:"].append(route_dict)
        current_idx += 1


    with open(path + "_" + str(W_H) + ".json", 'w') as json_file:
        json.dump(solution, json_file, indent=4)

def plot_results(results_file, instance_size):
    """Plots all the results of the specified instance size
    :param results_file: the path to the excel workbook containing all the results
    :param instance_size: the name of the sheet from the workbook that corresponds with the size of the instances"""
    df = pd.read_excel(results_file, instance_size)
    bar_width = 0.3
    index = range(len(df))

    plt.figure(figsize=(16, 8))

    if instance_size == "C5":
        y_limit = 260
    elif instance_size == "C10":
        y_limit = 430
    else:
        y_limit = 480

    plt.ylim(100, y_limit)

    bars_ALNS = plt.bar([i - 0.5 * bar_width for i in index], df['TD ALNS'], bar_width, label='ALNS TD', color='#2ca02c')
    bars_GUROBI = plt.bar([i + 0.5 * bar_width for i in index], df['TD GUROBI'], bar_width, label='GUROBI TD', color='#1f77b4')

    for idx, td in enumerate(df['TD ALNS comp']):
        plt.hlines(td, idx - bar_width, idx + 0.5 * bar_width, colors='red', linestyles='dashed')

    for idx, td in enumerate(df['TD GUROBI comp']):
        plt.hlines(td, idx + 0.5 * bar_width - 0.5 * bar_width, idx + 0.5 * bar_width + 0.5 * bar_width, colors='red', linestyles='dashed')

    plt.xlabel('Instance')
    plt.ylabel('TD')
    plt.xticks([i for i in index], df['instance'])

    for bar, num_vehicles in zip(bars_ALNS, df['vehicles ALNS']):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{int(num_vehicles)}', ha='center', va='bottom')

    for bar, num_vehicles in zip(bars_GUROBI, df['vehicles GUROBI']):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{int(num_vehicles)}', ha='center', va='bottom')

    handles, labels = plt.gca().get_legend_handles_labels()
    vehicles_handle = plt.Line2D([], [], color='white', label='Number of Vehicles (on top of bars)')
    comparison_handle = plt.Line2D([], [], color='red', linestyle='dashed', label='Results of Keskin and Çatay')
    handles.append(vehicles_handle)
    handles.append(comparison_handle)
    plt.legend(handles=handles)

    plt.savefig(f'..//..//Figures//{instance_size}_TD_scaled.png')
    plt.show()

def plot_results_battery_degradation(results_file, methodology, W_H):
    """plots the comparative results when battery degradation is considered
    :param results_file: the path to the results excel sheet
    :param methodology: "ALNS" if plotting results of ALNS, "GUROBI" if Gurobi results
    :param W_H: the W_H cost to indicate which results to plot"""
    df = pd.read_excel(results_file, "BD" + str(W_H))
    bar_width = 0.2
    instances = df['instance']

    td_alns = df['TD ALNS'].values
    bd_cost_alns = W_H * df['BD cost (W_L = 0.5, W_H = 1) ALNS'].values

    td_gurobi = df['TD GUROBI'].values
    bd_cost_gurobi = df['BD cost GUROBI'].values

    td_alns_simplified = df['TD ALNS BD simplified'].values
    bd_costs_alns_simplified = df['BD cost ALNS BD simplified'].values

    td_alns_BD = df['TD ALNS BD'].values
    bd_cost_alns_BD = df['BD cost ALNS BD'].values

    td_gurobi_BD = df['TD GUROBI BD'].values
    bd_cost_gurobi_BD = df['BD cost GUROBI BD'].values

    index = np.arange(len(instances))
    fig, ax = plt.subplots(figsize=(12, 6))

    if W_H == 0.2:
        y_UB = 550
    elif W_H == 1:
        y_UB = 700
    else:
        y_UB = 1000

    plt.ylim(100, y_UB)

    if methodology == "ALNS":
        ax.bar(index - bar_width, td_alns, bar_width, label='TD ALNS', color='#FFA500')
        ax.bar(index - bar_width, bd_cost_alns, bar_width, bottom=td_alns,
             label='Battery Degradation Costs ALNS benchmark', color="#CC8400")
        ax.bar(index, td_alns_simplified, bar_width, label='TD ALNS BD simplified', color='#32CD32')
        ax.bar(index, bd_costs_alns_simplified, bar_width, bottom=td_alns_simplified,
            label='Battery Degradation Costs ALNS BD simplified', color="#228B22")
        ax.bar(index + bar_width, td_alns_BD, bar_width, label='TD ALNS BD', color='#1E90FF')
        ax.bar(index + bar_width, bd_cost_alns_BD, bar_width, bottom=td_alns_BD,
            label='Battery Degradation Costs ALNS BD', color="#104E8B")
    elif methodology == "GUROBI":
        ax.bar(index - 0.5*bar_width, td_gurobi, bar_width, label='TD GUROBI', color='#FFA500')
        ax.bar(index - 0.5*bar_width, bd_cost_gurobi, bar_width, bottom=td_gurobi,
            label='Battery Degradation Costs GUROBI', color="#CC8400")
        ax.bar(index + 0.5*bar_width, td_gurobi_BD, bar_width, label='Distance Costs GUROBI BD', color='#1E90FF')
        ax.bar(index + 0.5*bar_width, bd_cost_gurobi_BD, bar_width, bottom=td_gurobi_BD,
            label='Battery Degradation Costs GUROBI BD', color="#104E8B")

    ax.set_xlabel('Instances')
    ax.set_ylabel('Costs')
    ax.set_xticks(index)
    ax.set_xticklabels(instances)
    ax.legend()

    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig(f'..//..//Figures//BD_alns_{W_H}.png')
    plt.show()

def random_instance_draw():
    """randomly selects small instances to use for EVRPTW-BD
    distribution of instance type and number of customers per instance is kept even
    :return the list of instances"""
    files = get_small_instance_file_names()
    selected = []
    rnd = random.Random()
    rnd.seed(42)
    prefixes = ["c", "r", "rc"]
    suffixes = ["C5", "C10", "C15"]
    sorted = {}

    for prefix in prefixes:
        for suffix in suffixes:
            sorted[(prefix, suffix)] = []

            for file in files:
                if file.startswith(prefix) and file.endswith(suffix):
                    if prefix != "r" or (prefix == "r" and file[1].isdigit()):
                        sorted[(prefix, suffix)].append(file)
                        files.remove(file)

    for options in sorted.values():
        selected_instance = random.choice(options)
        selected.append(selected_instance)

    return selected

def battery_degradation_cost_from_json_ALNS(filename, path, W_L, W_H):
    """calculates battery degradation costs, number of visits to the source and average charged quantity for ALNS solution
    :param filename: name of the instance
    :param path: the path of the solution's json file
    :param W_L: the low SoC BD cost
    :param W_H: the high SoC BD cost
    :return a tuple of these values in that order"""
    reader = Reader("evrptw_instances//" + filename + ".xlsx")

    with open(path, 'r') as file:
        solution = json.load(file)

    battery_capacity = reader.battery_capacity
    LB = 0.25*battery_capacity
    UB = 0.85*battery_capacity
    bd_cost = 0
    n_station_visits = 0
    soc_on_arrival = []
    soc_on_departure = []

    for route in solution["Routes:"]:
        bd_cost += W_H*(battery_capacity - UB)
        current_battery_level = battery_capacity
        current_location = 0

        for visit in route["Visits:"][1:-1]:
            current_battery_level -= reader.distance_between(current_location, visit["Location:"])

            if visit["Charged quantity:"] > 0:
                soc_on_arrival.append(current_battery_level/battery_capacity)
                n_station_visits += 1
                bd_cost += W_L*max(0, (LB - current_battery_level))
                current_battery_level += visit["Charged quantity:"]
                soc_on_departure.append(current_battery_level/battery_capacity)
                bd_cost += W_H*max(0, current_battery_level - UB)

            current_location = visit["Location:"]

        current_battery_level -= reader.distance_between(current_location, 0)
        bd_cost += W_L*max(0, (LB - current_battery_level))

    return bd_cost, n_station_visits, soc_on_arrival, soc_on_departure

def battery_degradation_cost_from_json_MILP(filename, path, W_L, W_H):
    """calculates battery degradation costs, number of visits to the source and average charged quantity for MILP solution
    :param filename: name of the instance
    :param path: the path of the solution's json file
    :param W_L: the low SoC BD cost
    :param W_H: the high SoC BD cost
    :return a tuple of these values in that order"""
    reader = Reader("evrptw_instances//" + filename + ".xlsx")

    with open(path, 'r') as file:
        solution = json.load(file)

    battery_capacity = reader.battery_capacity
    LB = 0.25 * battery_capacity
    UB = 0.85 * battery_capacity
    bd_cost = 0
    n_station_visits = 0
    soc_on_arrival = []
    soc_on_departure = []

    for route in solution["Routes:"]:
        for i, visit in enumerate(route["Visits:"]):
            charge_quantity = visit["Battery upon departure:"] - visit["Battery upon arrival:"]

            if charge_quantity > 0 and reader.type[visit["Location:"]] == "f":
                bd_cost += W_L * max(0, (LB - visit["Battery upon arrival:"]))
                soc_on_arrival.append(visit["Battery upon arrival:"]/battery_capacity)
                bd_cost += W_H * max(0, visit["Battery upon departure:"] - UB)
                soc_on_departure.append(visit["Battery upon departure:"]/battery_capacity)
                n_station_visits += 1

    return bd_cost, n_station_visits, soc_on_arrival, soc_on_departure

def heat_map_SoC(methodology, arrivals_or_departures):
    """Plots a heatmap that represents a frequency at which a vehicle arrives/departs to the charging station at a specific SoC interval
    :param methodology: 'ALNS' if plotting results of ALNS, 'GUROBI' if Gurobi results
    :param arrivals_or_departures:'arrivals', if plotting SoC on arrival, 'departures' if plotting SoC on departure"""
    files = ["c206C5", "r202C5", "rc204C5", "c101c10", "r201C10", "rc102C10", "c103C15", "r202C15", "rc202C15"]
    bd_costs = {"None": (0, 0), "Low": (0.1, 0.2), "Medium": (0.5, 1.0), "High": (2.5, 5.0)}
    soc_arrivals = {}
    soc_departures = {}

    for cost in bd_costs:
        soc_arrivals[cost] = []
        soc_departures[cost] = []

    for cost_level, cost in bd_costs.items():
        for file in files:
            if methodology == "ALNS":
                # adjusting the path to the file
                if cost_level == "Low":
                    W_H = str(cost[1])
                else:
                    W_H = str(int(cost[1]))

                if cost_level == "None":
                    path = "json_solutions//" + file + ".json"
                else:
                    path = "extension_solutions//" + file + "_" + W_H + ".json"
                bd, n_stat, soc_on_arrival, soc_on_departure = battery_degradation_cost_from_json_ALNS(file, path, cost[0], cost[1])
            elif methodology == "GUROBI":
                if cost_level == "None":
                    path = "MILP_solutions//" + file + "_" + str(0.2) + ".json"
                else:
                    path = "MILP_solutions_BD//" + file + "_" + str(cost[1]) + ".json"
                bd, n_stat, soc_on_arrival, soc_on_departure = battery_degradation_cost_from_json_MILP(file, path, cost[0], cost[1])
            else:
                raise ValueError

            soc_arrivals[cost_level].extend(soc_on_arrival)
            soc_departures[cost_level].extend(soc_on_departure)

    data_arrivals = {"SoC":  [item for sublist in soc_arrivals.values() for item in sublist],
                     "BD costs": [label for label in bd_costs.keys() for _ in range(len(soc_arrivals[label]))]}

    data_departures = {"SoC": [item for sublist in soc_departures.values() for item in sublist],
                     "BD costs": [label for label in bd_costs.keys() for _ in range(len(soc_departures[label]))]}

    if arrivals_or_departures == "arrivals":
        data = data_arrivals
    elif arrivals_or_departures == "departures":
        data = data_departures
    else:
        raise ValueError

    df = pd.DataFrame(data)
    cat_type = pd.CategoricalDtype(categories=['High', 'Medium', 'Low', 'None'], ordered=True)
    df['BD costs'] = df['BD costs'].astype(cat_type)
    intervals = [0, 0.25, 0.40, 0.55, 0.70, 0.85, 1]
    labels = ['0-25%', '25-40%', '40-55%', '55-70%', '70-85%', '85-100%']
    df['SoC Interval'] = pd.cut(df['SoC'], bins=intervals, labels=labels)
    complete_index = pd.MultiIndex.from_product([df['BD costs'].cat.categories, labels], names=['BD costs', 'SoC Interval'])
    heatmap_data = pd.DataFrame(index=complete_index, columns=['Count']).fillna(0)
    counts = df.groupby(['BD costs', 'SoC Interval']).size()

    for idx, count in counts.items():
        heatmap_data.loc[idx] = count

    heatmap_data = heatmap_data.reset_index().pivot(index='BD costs', columns='SoC Interval', values='Count')
    heatmap_data = heatmap_data.div(heatmap_data.sum(axis=1), axis=0)

    plt.figure(figsize=(10, 2))
    ax = sns.heatmap(heatmap_data, annot=True, cmap='coolwarm', cbar_kws={'label': 'Proportion'}, vmin=0, vmax=1)

    for tick in [1, 5]:
        ax.axvline(tick, color='red', linestyle='-', linewidth=2)

    plt.text(0.5, -0.5, 'Low SoC', fontsize=12, color='black', fontweight='bold', ha='center', va='center')
    plt.text(5.5, -0.5, 'High SoC', fontsize=12, color='black', fontweight='bold', ha='center', va='center')

    plt.xlabel('SoC Interval')
    plt.ylabel('BD costs')
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    plt.savefig(f'..//..//Figures//soc_departures_alns.png')
    plt.show()
