import numpy as numpy
import pandas as pandas


class Data(object):
    def __init__(self, sourceCSV):
        self.data = pandas.read_csv(sourceCSV)


    def getDataList(self):
        return self.data

    def getHeader(self):
        return self.data.columns

    def getDataByColumn(self, column):
        return self.data[column]

    def writeData(self, ncFile, variable, variableCreated):
        if 'value' in variable and variable['value'] != "":
            variableCreated[:] = self.convert_value(variable)
        elif 'csvcolumn' in variable and variable['csvcolumn'] != "":
            variableCreated[:] = self.getDataByColumn(variable['csvcolumn']).as_matrix()


    def convert_value(self, var):
        if var['typeof'] in ["str", "S1", "S"]:
            value = [ch for ch in str(var['value'])]
            value = numpy.array(value, 'S1')
        elif var['typeof'] == 'i':
            value = numpy.array(int(var['value']))
        else:
            value = numpy.array(float(var['value']))
        return (value)
