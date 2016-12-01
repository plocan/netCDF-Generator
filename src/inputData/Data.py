import csv

import numpy as numpy

from src.tools import tools


class Data(object):
    def __init__(self, sourceCSV):
        csvFile = csv.reader(open(sourceCSV), delimiter=',')
        self.header = csvFile.next()
        self.data = numpy.loadtxt(sourceCSV, delimiter=',', skiprows=2)

    def getDataList(self):
        return self.data

    def getHeader(self):
        return self.header

    def getDataByColumn(self, column):
        if column in self.data and self.data[column] != "":
            return self.data[:, column]

    def writeData(self, ncFile, variable, variableCreated):
        if 'value' in variable and variable['value'] != "":
            variableCreated[:] = self.convert_value(variable)
        elif 'csvcolumn' in variable and variable['csvcolumn'] != "":
            index = tools.indexvar(variable['csvcolumn'], self.header)
            variableCreated[:] = self.data[:, index]

    def convert_value(self, var):
        if var['typeof'] in ["str", "S1", "S"]:
            value = [ch for ch in str(var['value'])]
            value = numpy.array(value, 'S1')
        elif var['typeof'] == 'i':
            value = numpy.array(int(var['value']))
        else:
            value = numpy.array(float(var['value']))
        return (value)
