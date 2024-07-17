import numpy as np
import pandas as pd
import math
import config

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
        self.LB = config.lb*self.battery_capacity
        self.UB = config.ub*self.battery_capacity
        self.W_L = config.W_L
        self.W_H = config.W_H

    def number_of_service_points(self):
        """calculates how many service points the instance has
        :return: number of service points in the solution"""
        count = 0
        for i in range(self.n):
            if self.type[i] == "f":
                count += 1
        return count

    def distance_between(self, i, j):
        """returns the distance between locations i and j
        :param i: first location's index
        :param j: second location's index
        :return: distance"""
        x_i = self.x[i]
        x_j = self.x[j]
        y_i = self.y[i]
        y_j = self.y[j]
        return math.sqrt((x_i - x_j) ** 2 + (y_i - y_j) ** 2)

    def get_distance_matrix(self):
        """constructs a distance matrix, where i,j th element is
        the distance between locations i and j"""
        distances = np.zeros((self.n, self.n))

        for i in range(self.n):
            for j in range(self.n):
                distances[i, j] = self.distance_between(i, j)

        return distances

    def type_range(self, type="all"):
        """Gives the range of indexes for customers, sources or both, if not specified
        :param type: 'c', if looking at customers, 'f', if looking at stations, 'all' by default
        :return the range of indexes of specified type"""
        if type == "f":
            return range(1, self.n_service + 1)
        elif type == "c":
            return range(self.n_service + 1, self.n)
        else:
            return range(self.n)

    def find_closest(self, loc, available):
        """finds the closest location from available to location loc
        available might be a range object of specific type of locations
        :param loc: the location index of location under consideration
        :param available: a collection of locations from which we are looking for the closest one to loc
        :return the location index of the closest available location"""
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



