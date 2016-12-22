import numpy as numpy
import pandas as pandas

from src.Sort import Sort


class Data(object):
    def __init__(self, sourceCSV):
        self.data = pandas.read_csv(sourceCSV)
        self.appendPositions = {}

    def getDataByColumn(self, column):
        return self.data[column]

    def getHeader(self):
        return self.data.columns

    def writeData(self, variable, variableCreated):
        if 'value' in variable and variable['value'] != "":
            variableCreated[:] = self.convert_value(variable)
        else:
            column = Sort(self.data.columns).sortColumn(variable)
            variableCreated[:] = self.getDataByColumn(variable[column]).as_matrix()

        setattr(variableCreated, '_ChunkSizes', len(variableCreated[:]))
        if 'valid_max' in variable and 'valid_min' in variable:
            setattr(variableCreated, 'valid_max', numpy.amax(variableCreated))
            setattr(variableCreated, 'valid_min', numpy.amin(variableCreated))

    def appendData(self, variable, variableNetCDF, dimensions):
        elementLimit = dimensions.getSizeDimensions(variableNetCDF.dimensions[0]) - 1
        column = Sort(self.data.columns).sortColumn(variable)

        if 'value' in variable and variable['value'] != "":
            return 0
        dataNetCDF = pandas.DataFrame(variableNetCDF[:elementLimit + 1])
        dataCSV = pandas.Series(self.getDataByColumn(variable[column]))
        variableNetCDF[:] = pandas.concat([dataNetCDF, dataCSV], ignore_index=True, axis=0).as_matrix()
        setattr(variableNetCDF, '_ChunkSizes', len(variableNetCDF[:]))

    def appendDataInTheMiddle(self, variable, variableNetCDF, posCut, dimensions):
        if 'value' in variable and variable['value'] != "":
            return 0
        elementLimit = dimensions.getSizeDimensions(variableNetCDF.dimensions[0]) - 1
        dataNetCDF = variableNetCDF[:elementLimit + 1]
        firstMiddle = pandas.DataFrame(dataNetCDF[:posCut])
        secondMiddle = pandas.DataFrame(dataNetCDF[posCut:])
        column = Sort(self.data.columns).sortColumn(variable)
        dataCSV = pandas.Series(self.getDataByColumn(variable[column]))
        concat = pandas.concat([firstMiddle, dataCSV], ignore_index=True, axis=0)
        variableNetCDF[:] = pandas.concat([concat, secondMiddle], ignore_index=True, axis=0).as_matrix()
        setattr(variableNetCDF, '_ChunkSizes', len(variableNetCDF[:]))

    def appendDataToFileWithOldData(self, variable, variableNetCDF, posAppend, dimensions):
        if 'value' in variable and variable['value'] != "":
            return 0
        elementLimit = dimensions.getSizeDimensions(variableNetCDF.dimensions[0]) - 1
        dataNetCDF = variableNetCDF[:elementLimit + 1]

        column = Sort(self.data.columns).sortColumn(variable)

        if 'value' in variable and variable['value'] != "":
            return 0

        dataCSV = self.getDataByColumn(variable[column]).as_matrix()
        dataCSV = pandas.Series(dataCSV[posAppend:])
        variableNetCDF[:] = pandas.concat([pandas.DataFrame(dataNetCDF), dataCSV], ignore_index=True,
                                          axis=0).as_matrix()
        setattr(variableNetCDF, '_ChunkSizes', len(variableNetCDF[:]))

    def addAppendPostion(self, dimension, position):
        self.appendPositions[dimension] = position

    def convert_value(self, var):
        if var['typeof'] in ["str", "S1", "S"]:
            value = [ch for ch in str(var['value'])]
            value = numpy.array(value, 'S1')
        elif var['typeof'] == 'i':
            value = numpy.array(int(var['value']))
        else:
            value = numpy.array(float(var['value']))
        return (value)
