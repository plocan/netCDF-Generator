import numpy as numpy
import pandas as pandas
import sys

from Log import Log



from src.Sort import Sort


class Data_ego(object):
    def __init__(self, sourceCSV):

        self.data = pandas.read_csv(sourceCSV, encoding='utf-8')
        self.open_csv(sourceCSV)
        self.appendPositions = {}


    def open_csv(self, sourceCSV):
        self.data = pandas.read_csv(sourceCSV, encoding='utf-8')
        if len(self.get_header()) >  1:
            return
        self.data = pandas.read_csv(sourceCSV, encoding='utf-8', delim_whitespace=True)





    def get_data_by_column(self, column):
        insert = pandas.DataFrame();
        max = self.data["profilenumber"].max()
        for i in range(0, max):
            date = self.data.where(self.data["profilenumber"] == i)
            date = date.dropna()
            date = date.reset_index()
            # print  date["QC_chla"]
            insert.insert(i, i, date[column])
        return insert

    def get_header(self):
        return self.data.columns

    def write_data(self, variable, variableCreated):
        if 'value' in variable and variable['value'] != "":
            variableCreated[:] = self.convert_value(variable)
        else:
            column = Sort(self.data.columns).sort_column(variable)
            if column == -1:
                return
            variableCreated[:] = self.get_data_by_column(variable[column]).as_matrix()
        setattr(variableCreated, '_ChunkSizes', len(variableCreated[:]))

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

    def get_column(self):
        return self.data["profilenumber"].max()


    def get_row(self):
        date = self.data.where(self.data["profilenumber"] == 0)
        date = date.dropna()
        return len(date)