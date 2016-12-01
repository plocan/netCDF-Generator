import csv

import numpy as np


class Data(object):
    def __init__(self, sourceCSV):
        X = csv.reader(open(sourceCSV), delimiter=',')
        self.header = X.next()
        self.data = np.loadtxt(sourceCSV, delimiter=',', skiprows=2)

    def getDataList(self):
        return self.data

    def getHeader(self):
        return self.header

    def getDataByColumn(self, column):
        if column in self.data and self.data[column] != "":
            return self.data[:, column]
