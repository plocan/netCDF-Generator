import numpy as numpy
import pandas as pandas

from src.Sort import Sort


class Data(object):
    def __init__(self, sourceCSV):
        self.data = pandas.read_csv(sourceCSV, encoding='utf-8')
        self.appendPositions = {}

    def get_data_by_column(self, column):
        return self.data[column]

    def get_header(self):
        return self.data.columns

    def write_data(self, variable, variableCreated):
        try:
            if 'value' in variable and variable['value'] != "":
                variableCreated[:] = self.convert_value(variable)
            else:
                column = Sort(self.data.columns).sort_column(variable)
                variableCreated[:] = self.get_data_by_column(variable[column]).as_matrix()
            setattr(variableCreated, '_ChunkSizes', len(variableCreated[:]))
            if 'valid_max' in variable and 'valid_min' in variable:
                setattr(variableCreated, 'valid_max', numpy.amax(variableCreated))
                setattr(variableCreated, 'valid_min', numpy.amin(variableCreated))
        except:
            Log().set_log_error('Error writing data')
            Log().set_log_info('The script has closed unsatisfactorily')
            sys.exit(-1)

    def append_data(self, variable, variableNetCDF, dimensions):
        try:
            elementLimit = dimensions.get_size_dimensions(variableNetCDF.dimensions[0]) - 1
            column = Sort(self.data.columns).sort_column(variable)

            if 'value' in variable and variable['value'] != "":
                return 0
            dataNetCDF = pandas.DataFrame(variableNetCDF[:elementLimit + 1])
            dataCSV = pandas.Series(self.get_data_by_column(variable[column]))
            variableNetCDF[:] = pandas.concat([dataNetCDF, dataCSV], ignore_index=True, axis=0).as_matrix()
            setattr(variableNetCDF, '_ChunkSizes', len(variableNetCDF[:]))
        except:
            Log().set_log_error('Error adding data')
            Log().set_log_info('The script has closed unsatisfactorily')
            sys.exit(-1)

    def append_data_in_the_middle(self, variable, variableNetCDF, posCut, dimensions):
        try:
            if 'value' in variable and variable['value'] != "":
                return 0
            elementLimit = dimensions.get_size_dimensions(variableNetCDF.dimensions[0]) - 1
            dataNetCDF = variableNetCDF[:elementLimit + 1]
            firstMiddle = pandas.DataFrame(dataNetCDF[:posCut])
            secondMiddle = pandas.DataFrame(dataNetCDF[posCut:])
            column = Sort(self.data.columns).sort_column(variable)
            dataCSV = pandas.Series(self.get_data_by_column(variable[column]))
            concat = pandas.concat([firstMiddle, dataCSV], ignore_index=True, axis=0)
            variableNetCDF[:] = pandas.concat([concat, secondMiddle], ignore_index=True, axis=0).as_matrix()
            setattr(variableNetCDF, '_ChunkSizes', len(variableNetCDF[:]))
        except:
            Log().set_log_error('Error adding data')
            Log().set_log_info('The script has closed unsatisfactorily')
            sys.exit(-1)

    def append_data_to_file_with_old_data(self, variable, variableNetCDF, posAppend, dimensions):
        try:
            if 'value' in variable and variable['value'] != "":
                return 0
            elementLimit = dimensions.get_size_dimensions(variableNetCDF.dimensions[0]) - 1
            dataNetCDF = variableNetCDF[:elementLimit + 1]

            column = Sort(self.data.columns).sort_column(variable)

            if 'value' in variable and variable['value'] != "":
                return 0

            dataCSV = self.get_data_by_column(variable[column]).as_matrix()
            dataCSV = pandas.Series(dataCSV[posAppend:])
            variableNetCDF[:] = pandas.concat([pandas.DataFrame(dataNetCDF), dataCSV], ignore_index=True,
                                              axis=0).as_matrix()
            setattr(variableNetCDF, '_ChunkSizes', len(variableNetCDF[:]))
        except:
            Log().set_log_error('Error adding data')
            Log().set_log_info('The script has closed unsatisfactorily')
            sys.exit(-1)

    def add_append_position(self, dimension, position):
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
