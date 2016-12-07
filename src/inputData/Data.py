import numpy as numpy
import pandas as pandas

from src.inputData.Log import Log


class Data(object):
    def __init__(self, sourceCSV):
        self.data = pandas.read_csv(sourceCSV)


    def getDataList(self):
        return self.data

    def getHeader(self):
        return self.data.columns

    def getDataByColumn(self, column):
        return self.data[column]

    def isColumnExist(self, column):
        header = self.getHeader()
        if column in header:
            return True
        else:
            return False

    def writeData(self, ncFile, variable, variableCreated):
        if 'value' in variable and variable['value'] != "":
            variableCreated[:] = self.convert_value(variable)
        elif 'csvcolumn' in variable and variable['csvcolumn'] != "":
            variableCreated[:] = self.getDataByColumn(variable['csvcolumn']).as_matrix()
        elif 'variable_name' in variable and variable['variable_name'] != "" and self.isColumnExist(
                variable['variable_name']):
            variableCreated[:] = self.getDataByColumn(variable['variable_name']).as_matrix()
        elif 'standard_name' in variable and variable['standard_name'] != "" and self.isColumnExist(
                variable['standard_name']):
            variableCreated[:] = self.getDataByColumn(variable['standard_name']).as_matrix()
        else:
            Log().setLogWarning(
                'NETCDF: Not found column for: ' + variable['variable_name'] + ' standard name: ' + variable[
                    'standard_name'])


    def convert_value(self, var):
        if var['typeof'] in ["str", "S1", "S"]:
            value = [ch for ch in str(var['value'])]
            value = numpy.array(value, 'S1')
        elif var['typeof'] == 'i':
            value = numpy.array(int(var['value']))
        else:
            value = numpy.array(float(var['value']))
        return (value)
