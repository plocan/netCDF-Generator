import numpy as numpy
import sys

from Sort import Sort
from Log import Log


class Checker(object):
    def __init__(self, data):
        self.data = data
        self.appendDictionary = {}
        self.appendMiddleDictionary = {}

    # Comprobar si es el primer o ultimo elemento, testear bien. (Para perfiles)
    def checkPosTime(self, dimensions, variables, ncFile):
        sort = Sort(self.data.getHeader())
        variablesList = variables.variablesList
        for dimension in dimensions:
            if not dimension in variablesList or 'value' in variablesList[dimension] and variablesList[dimension][
                'value'] != "":
                self.appendMiddleDictionary[dimension] = -1
                continue
            variableNC = ncFile.variables[dimension]
            dataCSV = self.data.getDataByColumn(variablesList[dimension][sort.sortColumn(variablesList[dimension])])
            positionFirstElementBigger = numpy.where(variableNC[:][:] > dataCSV[:][0])
            positionFirstElement = numpy.where(variableNC[:][:] == dataCSV[:][0])
            if len(positionFirstElementBigger[0][:]) != 0 and len(positionFirstElement[0][:]) == 0:
                self.appendMiddleDictionary[dimension] = positionFirstElementBigger[0][0]
            else:
                self.appendMiddleDictionary[dimension] = 0
            self.appendDictionary[dimension] = 0

    def checkSameFile(self, dimensions, variables, ncFile):
        sort = Sort(self.data.getHeader())
        variablesList = variables.variablesList
        for dimension in dimensions:
            if not dimension in variablesList or 'value' in variablesList[dimension] and variablesList[dimension][
                'value'] != "":
                self.appendDictionary[dimension] = -1
                continue
            variableNC = ncFile.variables[dimension]
            dataCSV = self.data.getDataByColumn(variablesList[dimension][sort.sortColumn(variablesList[dimension])])
            firstElementCSV = numpy.where(variableNC[:][:] == dataCSV[:][0])
            lastElementNC = numpy.where(dataCSV[:][:] == variableNC[:][len(variableNC[:][:]) - 1])
            if len(firstElementCSV[0][:]) != 0 and len(lastElementNC[0][:]) != 0:
                if len(variableNC[:][:]) < len(dataCSV[:][:]):
                    self.appendDictionary[dimension] = lastElementNC[0][
                                                           0] + 1  # Comprobar si tengo que coger el ultimo del vector.
                    continue
                elif lastElementNC[0][0] < len(dataCSV[:][:]) - 1:
                    self.appendDictionary[dimension] = lastElementNC[0][
                                                           0] + 1  # Comprobar si tengo que coger el ultimo del vector.
                    continue
                elif len(variableNC[:][:]) == len(dataCSV[:][:]) or len(variableNC[:][:]) > len(dataCSV[:][:]):
                    Log().setLogInfo('This file has been used')
                    sys.exit(0)
            elif (len(firstElementCSV[0][:]) > 0 and len(lastElementNC[0][:]) == 0) or (
                            len(firstElementCSV[0][:]) == 0 and len(lastElementNC[0][:]) > 0):
                Log().setLogInfo('It is impossible append the information')
                sys.exit(0)
            self.appendDictionary[dimension] = 0

    def getAppendDictionary(self):
        return self.appendDictionary

    def getAppendMiddleDictionary(self):
        return self.appendMiddleDictionary

    def getAppendDictionaryElement(self, dimension):
        return self.appendDictionary[dimension]

    def getAppendMiddleDictionaryElement(self, dimension):
        return self.appendMiddleDictionary[dimension]
