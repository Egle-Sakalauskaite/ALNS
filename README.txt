Dear recruiters of Vinted Data Science and Analytics Academy,

this repository contains the code for my Bachelor thesis, the more signifficant part of it, the Adaptive Large Neighborhood Search (ALNS) algorithm was done using Python and it is probably the largest coding project I did entirely on my own. This algorithm aims to find a good solution for an Electric Vehicle Routing Problem with Time Windows and Partial Recharge (EVRPTW-PR), by iteratively destroying and repairing the initially built solution. In the destroy phaser, one of the Customer Removal (CR) or Station Removal (SR) operations are performed on the current solution. In the repair phase, removed customers are inserted (CI) and battery feasibility is restored by inserting recharging stations (SI). 

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




	
	
