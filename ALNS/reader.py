import pandas as pd
import math

class Reader:
    def __init__(self, path):
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

    def number_of_service_points(self):
        count = 0
        for i in range(self.n):
            if self.type[i] == "f":
                count += 1
        return count

    def distance_between(self, i, j):
        """returns the distance between i and j"""
        x_i = self.x[i]
        x_j = self.x[j]
        y_i = self.y[i]
        y_j = self.y[j]
        return math.sqrt((x_i - x_j) ** 2 + (y_i - y_j) ** 2)


    def type_range(self, type="all"):
        """Gives the range of indexes for customers, sources or both, if not specified"""
        if type == "f":
            return range(1, self.n_service + 1)
        elif type == "c":
            return range(self.n_service + 1, self.n)
        else:
            return range(self.n)

    def find_closest(self, loc, available):
        closest_loc = None
        closest_dist = 99999999999

        for i in available:
            if i == loc:
                continue

            distance = self.distance_between(loc, i)

            if distance < closest_dist:
                closest_dist = distance
                closest_loc = i

        return closest_loc

# data = Reader("evrptw_instances//c101_21.xlsx")
# data = Reader("evrptw_instances//c101C5.xlsx")

