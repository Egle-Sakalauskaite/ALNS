ALNS directory: contains the Python project for running ALNS
overview:
	- ALNS.py: main file for running ALNS
	- config.py: configuration file for switching between EVRPTW and EVRPTWBD and setting the battery degradation related parameters
	- helper.py: varios helper methods for running ALNS
	- reader.py: for creating Reader objects that store all parameters from the excel file
	- locationVisit.py: for creating and altering LocationVisit objects
	- route.py: for creating and altering Route objects that store multiple LocationVisit objects (active when BATTERY_DEGRADATION = False in config)
	- routeBD.py: for creating and altering Route objects that store multiple LocationVisit objects (active when BATTERY_DEGRADATION = True in config)
	- solution.py: for creating and altering Solution objects that store Route objects
	- customerRemoval.py: defines all CR operations
	- stationRemoval.py: defines all SR operations
	- customerInsertion.py: defines all CI operations
	- stationInsertion.py: defines all SI operations
	- tools.py: additional functions mostly for processing input and output data
	- evrptw_instances: all instance files (as excel sheets)
	- json_solutions: json files of the EVRPTW solutions
	- extension_solutions: json files of the EVRPTW-BD solutions

to run:
to run the ALNS algorithm. open ALNS.py. Specify the seed and a file (or multiple files) to run in files (e.g. files = ["c101C5", "c101C10"]). Keep in mind that if multiple files are specified, the seed will increment by 1 for each starting from the specified seed value.
To run all small instances, set seed = 42 and # files = tools.get_small_instance_file_names
to run EVRPTW-BD (extension), in config.py, set BATTERY_DEGRADATION = True and specify desired parameters, then run ALNS.py. After the algorithm terminates, the best solution will be checked for feasibility and printed in the terminal, as well as saved as a json file in json_solutions if config.BATTERY_DEGRADATION = False, or extension_solutions, if config.BATTERY_DEGRADATION = True.

to avoid results being influenced by the seed of the RNG, seed varries per instance:
instance: seed
c101C5: 42, c103C5: 43, c101C10: 44, c104C10: 45, c103C15: 46, c106C15: 47
c206C5: 48, c208C5: 49, c202C10: 50, c205C10: 51, c202C15: 52, c208C15: 53
r104C5: 54, r105C5: 55, r102C10: 56, r103C10: 57, r102C15: 58, r105C15: 59
r202C5: 60, r203C5: 61, r201C10: 62, r203C10: 63, r202C15: 64, r209C15: 65
rc105C5: 66, rc108C5: 67, rc102C10: 68, rc108C10: 69, rc103C15: 70, rc108C15: 71
rc204C5: 72, rc208C5: 73, rc201C10: 74, rc205C10: 75, rc202C15: 76, rc204C15: 77

c101C100: 42, c201C100: 43, r101C100: 44, r201C100: 45, rc101:C100: 46, rc201C100: 47

for EVRPTW-BD seed varries per instance, but all 3 sizes of battery degradation costs are run with the same seed:

c101C10: 42, c103C15: 43, c206C5: 44, r202C5: 45, r201C10: 46, r202C15: 47, rc102C10: 48, rc204C5: 49, rc202C15: 50



MILP directory: contains the Java project for running MILP
overview:
	- src: source code
		- Main: main file for solving MILP for EVRPTW and EVRPTW-BD with Gurobi
		- Helper: various files for reading and processing parameter data
	- evrptw_instances: all instance files (as csv files)
	- models: lp files of EVRPTW
	- decision_variables: raw Gurobi output of best found solutions for EVRPTW (decision variables == 0 are skipped)
	- decision_variables_reoptimized: raw Gurobi output for reoptimized battery levels on arrival and departure of an existing EVRPTW solution (decision variables == 0 are skipped)
	- decision_variables_BD: raw Gurobi output of best found solutions for EVRPTW_BD (decision variables == 0 are skipped)
	- MILP_solutions: json files of the EVRPTW solutions
	- MILP_solutions: json files of the EVRPTW-BD solutions

to run:
open Main.py, remove the comment markers from the files you wish to run and run the function solve() for EVRPTW. To solve for EVRPTW-BD. additionally specify desired price_idx and run the function solve_extension(). To reoptimize battery level upon arrival and departure for an existing EVRPTW solution in order to obtain accurate BD costs, run solve_BD_cost_for_existing_solutio()

price_idx	W_L	W_H
0		0.1	0.2
1		0.5	1
2		2.5	5


	
	