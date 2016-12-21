import os
import sys

from netCDF4._netCDF4 import Dataset

from Data import *
from Log import Log
from Metadata import *


class NetCDFConverter(object):
    def __init__(self, metadataFile, csvFile, ncOutput):
        Log().setLogInfo("[Begin] conversion to NetCDF of: " + metadataFile + "  " + csvFile + "  " + ncOutput)
        self.ncOutput = ncOutput
        self.checkSource(metadataFile, csvFile)
        self.metadata = Metadata(metadataFile)
        self.metadataData = self.metadata.getMetadata()
        self.data = Data(csvFile)
        self.ncOutput = self.ncOutput + self.metadata.getGlobalAttributes().getID() + ".nc"
        self.version = self.metadata.getGlobalAttributes().getNetCDFVersion().replace(" ", "_")

        if not os.path.exists(self.ncOutput):
            self.ncFile = Dataset(self.ncOutput, 'w', format='NETCDF' + self.version)
            self.dimensions = self.metadata.getDimensions()
            self.globalAttributes = Metadata(metadataFile).getGlobalAttributes()
            self.globalAttributes.writeAttributes(self.ncFile)
            self.dimensions.writeDimensions(self.ncFile)
            self.variables = self.metadata.getVariables()
            self.writeVariablesData()
        else:
            self.ncFile = Dataset(self.ncOutput, 'r+')
            self.writeAppendVariablesData()

        Log().setLogInfo("[Finished] conversion to NetCDF of : " + metadataFile + "  " + csvFile + "  " + ncOutput)

    def writeVariablesData(self):
        variables = self.metadataData['variables']
        variablesNames = ['_FillValue', 'variable_name', 'typeof', 'dim', 'value', 'csvcolumn']

        for variable in variables:
            variableCreated = self.variables.writeVariables(self.ncFile, variable, self.version)
            self.data.writeData(variable, variableCreated)
            self.variables.deleteAttributes(variablesNames, variable)
            self.variables.addAttributeToVariable(variableCreated, variable)

    def checkSource(self, metadataFile, csvFile):
        if not os.path.exists(metadataFile):
            Log().setLogError('Not found .json file. (Metadata file)')
            Log().setLogInfo('The script has closed unsatisfactorily')
            sys.exit(-1)
        elif not os.path.exists(csvFile):
            Log().setLogError('Not .csv / .data file. (Data file)')
            Log().setLogInfo('The script has closed unsatisfactorily')
            sys.exit(-1)
        finalCharacter = self.ncOutput[len(self.ncOutput) - 1]
        if finalCharacter != '/':
            self.ncOutput += '/'

    def writeAppendVariablesData(self):
        variables = self.metadataData['variables']

        for variable in variables:
            if 'standard_name' in variable and variable['standard_name'] == 'time':
                posCut = self.checkPosTime(variable, self.ncFile.variables[variable['variable_name']])
                posAppend = self.checkSameFile(variable, self.ncFile.variables[variable['variable_name']])
            if posCut == -1 and posAppend == 0:
                self.data.appendData(variable, self.ncFile.variables[variable['variable_name']])
            elif posAppend > 0:
                self.data.appendDataToFileWithOldData(variable, self.ncFile.variables[variable['variable_name']],
                                                      posAppend)
            else:
                self.data.appendDataInTheMiddle(variable, self.ncFile.variables[variable['variable_name']], posCut)

    def checkPosTime(self, variable, variableNC):
        if not 'csvcolumn' in variable and variable['csvcolumn'] != 'time':
            return -1
        dataCSV = self.data.getDataByColumn(variable['csvcolumn'])
        pos = numpy.where(variableNC[:][:] > dataCSV[:][0])
        if len(pos[0][:]) != 0:
            return pos[0][0]
        else:
            return -1

    def checkSameFile(self, variable, variableNC):
        if not 'csvcolumn' in variable and variable['csvcolumn'] != 'time':
            return -1

        dataCSV = self.data.getDataByColumn(variable['csvcolumn']).as_matrix()

        pos = numpy.where(variableNC[:][:] == dataCSV[:][0])
        pos2 = numpy.where(dataCSV[:][:] == variableNC[:][len(variableNC[:][:]) - 1])
        if len(pos[0][:]) != 0 and len(pos2[0][:]) != 0:
            if len(variableNC[:][:]) < len(dataCSV[:][:]):
                return pos2[0][0] + 1
            elif pos2[0][0] < len(dataCSV[:][:]) - 1:
                return pos2[0][0] + 1
            elif len(variableNC[:][:]) == len(dataCSV[:][:]) or len(variableNC[:][:]) > len(dataCSV[:][:]):
                Log().setLogInfo('This file has been used')
                sys.exit(0)
        elif (len(pos[0][:]) > 0 and len(pos2[0][:]) != 0) or (len(pos[0][:]) != 0 and len(pos2[0][:]) > 0):
            Log().setLogInfo('It is impossible append the information')
            sys.exit(0)
        else:
            return 0


if __name__ == '__main__':
    NetCDFConverter('/Users/Loedded/Downloads/xx.json', '/Users/Loedded/Downloads/xx.dat', '/Users/Loedded/Downloads')

"""
if __name__ == '__main__':
    NetCDFConverter(sys.argv[1], sys.argv[2], sys.argv[3])"""
