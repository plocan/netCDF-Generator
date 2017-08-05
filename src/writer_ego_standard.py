from Checker import Checker
import numpy as numpy
import pandas as pandas
import sys

class writer_ego_standard(object):

    def __init__(self, dimensions):
        self.STRING = {"STRING2" : 2, "STRING4" : 4, "STRING8" : 8, "STRING16" : 16,
                       "STRING32" : 32, "STRING64" : 64, "STRING128" : 128,
                       "STRING256" : 256, "STRING1024" : 1024, "DATE_TIME" : 14}
        self.dimension = dimensions


    def write(self, variables, value, ncFile):
        variablesNames = ['_FillValue', 'variable_name', 'typeof', 'dim', 'value', 'csvcolumn']
        for var in variables:
            variable = variables[var]
            dimension = Checker().check_dimensions(variable)
            if dimension != "":
                variablesNames[3] = dimension

            fillVal = variable['_FillValue'] if '_FillValue' in variable and variable['_FillValue'] != "" else False
            dimension = Checker().check_dimensions(variable)
            if dimension != "":
                if not type(variable[dimension]) is list and variable[dimension] in self.STRING:
                    variableCreated = ncFile.createVariable(variable['variable_name'], variable['typeof'],
                                                            (variable[dimension]),
                                                            fill_value=fillVal, zlib=True, complevel=9)
                    variableCreated[:] = self.convert_value(variable, value[variable['variable_name']])
                elif len(variable[dimension]) == 2:
                    variableCreated = ncFile.createVariable(variable['variable_name'], variable['typeof'],
                                                            (variable[dimension]),
                                                            fill_value=fillVal, zlib=True, complevel=9)
                    variableCreated[:] = self.convert_value_matrix(variable, value[variable['variable_name']])
                else:
                    variableCreated = ncFile.createVariable(variable['variable_name'], variable['typeof'], (variable[dimension]),
                                                   fill_value=float(fillVal), zlib=True, complevel=9)
                    variableCreated[:] = self.convert_value(variable, value[variable['variable_name']])
            else:
                if variable['typeof'] == "byte":
                    variableCreated = ncFile.createVariable(variable['variable_name'], variable['typeof'],
                                                            fill_value=float(fillVal),
                                                            zlib=True, complevel=9)
                elif variable['typeof'] == "S1":
                    variableCreated = ncFile.createVariable(variable['variable_name'], variable['typeof'],
                                                            fill_value=fillVal,
                                                            zlib=True, complevel=9)
                else:
                    variableCreated = ncFile.createVariable(variable['variable_name'], variable['typeof'],
                                                       fill_value=bytes(fillVal),
                                                       zlib=True, complevel=9)
                variableCreated[:] = self.convert_value(variable, value[variable['variable_name']])


            for key in variablesNames:
                if key in variable:
                    del variable[key]

            for attribute in variable:
                if variable[attribute]:
                    setattr(variableCreated, attribute, variable[attribute])


    def convert_value(self, var, val):
        if var['dim'] != '':
            if var['typeof'] in ["str", "S1", "S"]:
                value = [ch for ch in str(val)]
                if(len(value) < self.STRING[var['dim']]):
                    while len(value) < self.STRING[var['dim']]:
                        value = numpy.append(value, '')
                value = numpy.array(value, 'S1')
            elif var['typeof'] == 'i':
                value = numpy.array(int(val))
            else:
                value = numpy.array(float(val))
            return (value)
        else:
            if var['typeof'] in ["str", "S1", "S"]:
                value = [ch for ch in str(val)]
                value = numpy.array(value, 'S1')
            elif var['typeof'] == 'i':
                value = numpy.array(int(val))
            elif var['typeof'] == 'byte':
                value = numpy.array(bytes(val))
            else:
                value = numpy.array(float(val))
            return (value)

    def convert_value_matrix(self, var, val):
        if var['dim'] != '':
            if var['typeof'] in ["str", "S1", "S"]:
                dim = var['dim']
                if dim[0] in self.dimension:
                    first = dim[0]
                    second = dim[1]
                else:
                    second = dim[0]
                    first = dim[1]
                if not type(val) is list:
                    for i in range(0, self.dimension[first]):
                        value = [ch for ch in str(val)]
                        if (len(value) < self.STRING[second]):
                            while len(value) < self.STRING[second]:
                                value = numpy.append(value, '')
                        value = numpy.array(value, 'S1')
                elif len(val) == 0:
                    return
                else:
                    insert = pandas.DataFrame();
                    for i in range(0, self.dimension[first]):
                        value = [ch for ch in str(val[i])]
                        if (len(value) < self.STRING[second]):
                            while len(value) < self.STRING[second]:
                                value = numpy.append(value, '')
                        insert.insert(i, i, value)
                    value = numpy.array(insert, 'S1')
            elif var['typeof'] == 'i':
                value = numpy.array(int(val))
            else:
                value = numpy.array(float(val))
            return (value)