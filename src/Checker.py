import os

import numpy as numpy
import sys

from Sort import Sort
from Log import Log


class Checker(object):
    def __init__(self, data=None):
        if not data is None:
            self.data = data
        self.appendDictionary = {}
        self.appendMiddleDictionary = {}

    # Check if it is the first or last item, test well. (For Profiles)
    def check_position_time(self, dimensions, variables, ncFile):
        try:
            sort = Sort(self.data.get_header())
            variablesList = variables.variablesList
            for dimension in dimensions:
                if not dimension in variablesList or 'value' in variablesList[dimension] and variablesList[dimension][
                    'value'] != "":
                    self.appendMiddleDictionary[dimension] = -1
                    continue
                variableNC = ncFile.variables[dimension]
                dataCSV = self.data.get_data_by_column(variablesList[dimension][sort.sort_column(variablesList[dimension])])
                positionFirstElementBigger = numpy.where(variableNC[:][:] > dataCSV[:][0])
                positionFirstElement = numpy.where(variableNC[:][:] == dataCSV[:][0])
                if len(positionFirstElementBigger[0][:]) != 0 and len(positionFirstElement[0][:]) == 0:
                    self.appendMiddleDictionary[dimension] = positionFirstElementBigger[0][0]
                else:
                    self.appendMiddleDictionary[dimension] = 0
                self.appendDictionary[dimension] = 0
        except:
            Log().set_log_error('Error dimensions not found')
            Log().set_log_info('The script has closed unsatisfactorily')
            sys.exit(-1)

    def check_same_file(self, dimensions, variables, ncFile):
        sort = Sort(self.data.get_header())
        variablesList = variables.variablesList
        for dimension in dimensions:
            if not dimension in variablesList or 'value' in variablesList[dimension] and variablesList[dimension][
                'value'] != "":
                self.appendDictionary[dimension] = -1
                continue
            variableNC = ncFile.variables[dimension]
            dataCSV = self.data.get_data_by_column(variablesList[dimension][sort.sort_column(variablesList[dimension])])
            firstElementCSV = numpy.where(variableNC[:][:] == dataCSV[:][0])
            lastElementNC = numpy.where(dataCSV[:][:] == variableNC[:][len(variableNC[:][:]) - 1])
            if len(firstElementCSV[0][:]) != 0 and len(lastElementNC[0][:]) != 0:
                if len(variableNC[:][:]) < len(dataCSV[:][:]):
                    self.appendDictionary[dimension] = lastElementNC[0][0] + 1
                    continue
                elif lastElementNC[0][0] < len(dataCSV[:][:]) - 1:
                    self.appendDictionary[dimension] = lastElementNC[0][0] + 1
                    continue
                elif len(variableNC[:][:]) == len(dataCSV[:][:]) or len(variableNC[:][:]) > len(dataCSV[:][:]):
                    Log().set_log_info('This file has been used')
                    sys.exit(0)
            elif (len(firstElementCSV[0][:]) > 0 and len(lastElementNC[0][:]) == 0) or (
                            len(firstElementCSV[0][:]) == 0 and len(lastElementNC[0][:]) > 0):
                Log().set_log_info('It is impossible append the information')
                sys.exit(0)
            self.appendDictionary[dimension] = 0

    def check_source(self, metadataFile, csvFile, ncOutput):
        if not os.path.exists(metadataFile):
            Log().set_log_error('Not found .json file. (Metadata file)')
            Log().set_log_info('The script has closed unsatisfactorily')
            sys.exit(-1)
        elif not os.path.exists(csvFile):
            Log().set_log_error('Not .csv / .data file. (Data file)')
            Log().set_log_info('The script has closed unsatisfactorily')
            sys.exit(-1)
        finalCharacter = ncOutput[len(ncOutput) - 1]
        if finalCharacter != '/':
            ncOutput += '/'
            return ncOutput
        return ncOutput

    def check_dimensions(self, variable):
        if 'dim' in variable and variable['dim'] != "":
            return 'dim'
        elif 'dimensions' in variable and variable['dimensions'] != "":
            return 'dimensions'
        else:
            return ""

    def get_append_dictionary(self):
        return self.appendDictionary

    def get_append_middle_dictionary(self):
        return self.appendMiddleDictionary

    def get_append_dictionary_element(self, dimension):
        return self.appendDictionary[dimension]

    def get_append_middle_dictionary_element(self, dimension):
        return self.appendMiddleDictionary[dimension]

