import os

import sys
from netCDF4._netCDF4 import Dataset

from src.inputData.Data import *
from src.inputData.Log import Log
from src.inputData.Metadata import *


class NetCDFConverter(object):
    def __init__(self, metadataFile, csvFile, ncOutput):
        Log().setLogInfo("[Begin] conversion to NetCDF of: " + metadataFile + "  " + csvFile + "  " + ncOutput)
        self.ncOutput = ncOutput
        self.checkSource(metadataFile, csvFile)

        self.metadata = Metadata(metadataFile)
        self.metadataData = self.metadata.getMetadata()
        self.data = Data(csvFile)

        self.ncOutput = self.ncOutput + self.metadata.getGlobalAttributes().getID() + ".nc"
        self.version = self.metadata.getGlobalAttributes().getNetCDFVersion()
        if self.version == '3':
            self.format = '3_CLASSIC'
        else:
            self.format = '4'

        if os.path.exists(self.ncOutput) == False:
            self.ncFile = Dataset(self.ncOutput, 'w', format='NETCDF' + self.format)

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
            self.data.writeData(self.ncFile, variable, variableCreated, self.version)
            self.variables.deleteAttributes(variablesNames, variable)
            self.variables.addAttributeToVariable(variableCreated, variable)

    def checkSource(self, metadataFile, csvFile):
        if os.path.exists(metadataFile) == False:
            Log().setLogError('Not found .json file. (Metadata file)')
            Log().setLogInfo('The script has closed unsatisfactorily')
            sys.exit(-1)
        elif os.path.exists(csvFile) == False:
            Log().setLogError('Not .csv / .data file. (Data file)')
            Log().setLogInfo('The script has closed unsatisfactorily')
            sys.exit(-1)
        finalCharacter = self.ncOutput[len(self.ncOutput) - 1]
        if finalCharacter != '/':
            self.ncOutput = self.ncOutput + '/'

    def writeAppendVariablesData(self):
        variables = self.metadataData['variables']

        for variable in variables:
            self.data.appendData(variable, self.ncFile.variables[variable['variable_name']],
                                 getattr(self.ncFile.variables[variable['variable_name']], '_ChunkSizes'))


if __name__ == '__main__':
    NetCDFConverter('/Users/Loedded/Downloads/xx.json', '/Users/Loedded/Downloads/xx.dat',
                    '/Users/Loedded/Downloads')
