import numpy as numpy
import pandas as pandas
import sys

from Log import Log


class Data(object):
    def __init__(self, sourceCSV):
        self.data = pandas.read_csv(sourceCSV)

    def getDataByColumn(self, column):
        return self.data[column]

    def writeData(self, variable, variableCreated):
        try:
            if 'value' in variable and variable['value'] != "":
                variableCreated[:] = self.convert_value(variable)
            elif 'csvcolumn' in variable and variable['csvcolumn'] != "":
                variableCreated[:] = self.getDataByColumn(variable['csvcolumn']).as_matrix()
            elif 'variable_name' in variable and variable['variable_name'] != "":
                variableCreated[:] = self.getDataByColumn(variable['variable_name']).as_matrix()
            elif 'standard_name' in variable and variable['standard_name'] != "":
                variableCreated[:] = self.getDataByColumn(variable['standard_name']).as_matrix()
            else:
                Log().setLogWarning(
                    'NETCDF: Not found column for: ' + variable['variable_name'] + ' standard name: ' + variable[
                        'standard_name'])
            setattr(variableCreated, '_ChunkSizes', len(variableCreated[:]))
            if 'valid_max' in variable and 'valid_min' in variable:
                setattr(variableCreated, 'valid_max', numpy.amax(variableCreated))
                setattr(variableCreated, 'valid_min', numpy.amin(variableCreated))
        except:
            Log().setLogError('Wrong variable type')
            Log().setLogInfo('The script has closed unsatisfactorily')
            sys.exit(-1)

    def appendData(self, variable, variableNetCDF):
        elementLimit = numpy.nonzero(variableNetCDF[:])
        elementLimit = elementLimit[0][len(elementLimit[0]) - 1]
        posFillValue = variable['_FillValue'] if '_FillValue' in variable and variable['_FillValue'] != "" else False
        posFillValue = numpy.where(variableNetCDF[:] == posFillValue)
        if len(posFillValue[0][:]) > 0:
            elementLimit = posFillValue[0][len(posFillValue[0]) - 1] - 1

        if 'value' in variable and variable['value'] != "":
            return 0
        elif 'csvcolumn' in variable and variable['csvcolumn'] != "":
            dataNetCDF = pandas.DataFrame(variableNetCDF[:elementLimit + 1])
            dataCSV = pandas.Series(self.getDataByColumn(variable['csvcolumn']))
            variableNetCDF[:] = pandas.concat([dataNetCDF, dataCSV], ignore_index=True, axis=0).as_matrix()
        elif 'variable_name' in variable and variable['variable_name'] != "":
            dataNetCDF = pandas.DataFrame(variableNetCDF[:elementLimit + 1])
            dataCSV = pandas.Series(self.getDataByColumn(variable['variable_name']))
            variableNetCDF[:] = pandas.concat([dataNetCDF, dataCSV], ignore_index=True, axis=0).as_matrix()
        elif 'standard_name' in variable and variable['standard_name'] != "":
            dataNetCDF = pandas.DataFrame(variableNetCDF[:elementLimit + 1])
            dataCSV = pandas.Series(self.getDataByColumn(variable['standard_name']))
            variableNetCDF[:] = pandas.concat([dataNetCDF, dataCSV], ignore_index=True, axis=0).as_matrix()
        else:
            Log().setLogWarning(
                'NETCDF: Not found column for: ' + variable['variable_name'] + ' standard name: ' + variable[
                    'standard_name'])
        setattr(variableNetCDF, '_ChunkSizes', len(variableNetCDF[:]))

    def appendDataInTheMiddle(self, variable, variableNetCDF, posCut):
        elementLimit = numpy.nonzero(variableNetCDF[:])
        elementLimit = elementLimit[0][len(elementLimit[0]) - 1]
        posFillValue = variable['_FillValue'] if '_FillValue' in variable and variable['_FillValue'] != "" else False
        posFillValue = numpy.where(variableNetCDF[:] == posFillValue)
        if len(posFillValue[0][:]) > 0:
            elementLimit = posFillValue[0][len(posFillValue[0]) - 1] - 1

        dataNetCDF = variableNetCDF[:elementLimit + 1]

        firstMiddle = pandas.DataFrame(dataNetCDF[:posCut])
        secondMiddle = pandas.DataFrame(dataNetCDF[posCut:])

        if 'value' in variable and variable['value'] != "":
            return 0
        elif 'csvcolumn' in variable and variable['csvcolumn'] != "":
            dataCSV = pandas.Series(self.getDataByColumn(variable['csvcolumn']))
            concat = pandas.concat([firstMiddle, dataCSV], ignore_index=True, axis=0)
            variableNetCDF[:] = pandas.concat([concat, secondMiddle], ignore_index=True, axis=0).as_matrix()

        elif 'variable_name' in variable and variable['variable_name'] != "":
            dataCSV = pandas.Series(self.getDataByColumn(variable['variable_name']))
            concat = pandas.concat([firstMiddle, dataCSV], ignore_index=True, axis=0)
            variableNetCDF[:] = pandas.concat([concat, secondMiddle], ignore_index=True, axis=0).as_matrix()

        elif 'standard_name' in variable and variable['standard_name'] != "":
            dataCSV = pandas.Series(self.getDataByColumn(variable['standard_name']))
            concat = pandas.concat([firstMiddle, dataCSV], ignore_index=True, axis=0)
            variableNetCDF[:] = pandas.concat([concat, secondMiddle], ignore_index=True, axis=0).as_matrix()
        else:
            Log().setLogWarning(
                'NETCDF: Not found column for: ' + variable['variable_name'] + ' standard name: ' + variable[
                    'standard_name'])
        setattr(variableNetCDF, '_ChunkSizes', len(variableNetCDF[:]))

    def appendDataToFileWithOldData(self, variable, variableNetCDF, posAppend):
        elementLimit = numpy.nonzero(variableNetCDF[:])
        elementLimit = elementLimit[0][len(elementLimit[0]) - 1]
        dataNetCDF = variableNetCDF[:elementLimit + 1]

        posFillValue = variable['_FillValue'] if '_FillValue' in variable and variable['_FillValue'] != "" else False
        posFillValue = numpy.where(dataNetCDF[:] == posFillValue)
        if len(posFillValue[0][:]) > 0:
            elementLimit = posFillValue[0][len(posFillValue[0]) - 1] - 1
            dataNetCDF = variableNetCDF[:elementLimit + 1]

        if 'value' in variable and variable['value'] != "":
            return 0
        elif 'csvcolumn' in variable and variable['csvcolumn'] != "":
            dataCSV = self.getDataByColumn(variable['csvcolumn']).as_matrix()
            dataCSV = pandas.Series(dataCSV[posAppend:])
            variableNetCDF[:] = pandas.concat([pandas.DataFrame(dataNetCDF), dataCSV], ignore_index=True,
                                              axis=0).as_matrix()
        elif 'variable_name' in variable and variable['variable_name'] != "":
            dataCSV = self.getDataByColumn(variable['variable_name']).as_matrix()
            dataCSV = pandas.Series(dataCSV[posAppend:])
            variableNetCDF[:] = pandas.concat([pandas.DataFrame(dataNetCDF), dataCSV], ignore_index=True,
                                              axis=0).as_matrix()
        elif 'standard_name' in variable and variable['standard_name'] != "":
            dataCSV = self.getDataByColumn(variable['standard_name']).as_matrix()
            dataCSV = pandas.Series(dataCSV[posAppend:])
            variableNetCDF[:] = pandas.concat([pandas.DataFrame(dataNetCDF), dataCSV], ignore_index=True,
                                              axis=0).as_matrix()
        else:
            Log().setLogWarning(
                'NETCDF: Not found column for: ' + variable['variable_name'] + ' standard name: ' + variable[
                    'standard_name'])
        setattr(variableNetCDF, '_ChunkSizes', len(variableNetCDF[:]))

    def convert_value(self, var):
        if var['typeof'] in ["str", "S1", "S"]:
            value = [ch for ch in str(var['value'])]
            value = numpy.array(value, 'S1')
        elif var['typeof'] == 'i':
            value = numpy.array(int(var['value']))
        else:
            value = numpy.array(float(var['value']))
        return (value)
