import numpy as np
import pandas as pd
import math

class Reader:
    def __init__(self, path):
        """initializes all instance data
        :param path: path to the excel file"""
        df = pd.read_excel(path, "locations")
        other = pd.read_excel(path, "other")
        self.type = df['Type'].values
        self.x = df['x'].values
        self.y = df['y'].values
        self.demand = df['demand'].values
        self.ready_time = df['ReadyTime'].values
        self.due_time = df['DueDate'].values
        self.service_time = df['ServiceTime'].values
        self.n = len(self.type)
        self.n_service = self.number_of_service_points()
        self.n_customer = self.n - self.n_service - 1
        self.battery_capacity = other['Q'][0]
        self.load_capacity = other['C'][0]
        self.battery_consumption_rate = other['r'][0]
        self.recharging_rate = other['g'][0]
        self.velocity = other['v'][0]
        self.distance_matrix = self.get_distance_matrix()

    def number_of_service_points(self):
        """calculates how many service points the instance has"""
        count = 0
        for i in range(self.n):
            if self.type[i] == "f":
                count += 1
        return count

    def distance_between(self, i, j):
        """returns the distance between i and j
        :param i: first location's index
        :param j: second location's index'"""
        x_i = self.x[i]
        x_j = self.x[j]
        y_i = self.y[i]
        y_j = self.y[j]
        return math.sqrt((x_i - x_j) ** 2 + (y_i - y_j) ** 2)
    def get_distance_matrix(self):
        distances = np.zeros((self.n, self.n))

        for i in range(self.n):
            for j in range(self.n):
                distances[i, j] = self.distance_between(i, j)

        return distances

    def type_range(self, type="all"):
        """Gives the range of indexes for customers, sources or both, if not specified
        :param type: 'c', if looking at customers, 'f', if looking at stations, 'all' by default"""
        if type == "f":
            return range(1, self.n_service + 1)
        elif type == "c":
            return range(self.n_service + 1, self.n)
        else:
            return range(self.n)

    def find_closest(self, loc, available):
        """finds the closest location from available to location loc
        :param loc: the location index of location under consideration
        :param available: a collection of locations from which we are looking for the closest one to loc"""
        closest_loc = None
        closest_dist = 99999999999

        for i in available:
            if i == loc:
                continue

            distance = self.distance_matrix[loc, i]

            if distance < closest_dist:
                closest_dist = distance
                closest_loc = i

        return closest_loc

# path = "evrptw_instances//" + "c101c5" + ".xlsx"
# data = Reader(path)
#
# dist = 2*data.distance_between(0, 4)
# dist += data.distance_between(0, 5)
# dist += data.distance_between(5, 2)
# dist += data.distance_between(2, 6)
# dist += data.distance_between(6, 0)
# dist += 2*data.distance_between(0, 7)
# dist += 2*data.distance_between(0, 8)