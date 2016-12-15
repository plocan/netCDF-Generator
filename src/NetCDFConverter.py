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
        try:
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
        except:
            Log().setLogError("FATAL ERROR")
            Log().setLogInfo('The script has closed unsatisfactorily')
            self.deleteNcFile()
            sys.exit(-1)
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
            self.data.appendData(variable, self.ncFile.variables[variable['variable_name']])

if __name__ == '__main__':
    NetCDFConverter(sys.argv[1], sys.argv[2], sys.argv[3])
