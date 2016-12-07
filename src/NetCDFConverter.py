import os

from netCDF4 import Dataset, sys

from src.inputData.Data import *
from src.inputData.Log import Log
from src.inputData.Metadata import *


class NetCDFConverter(object):
    def __init__(self, metadataFile, csvFile, ncOutput):
        Log().setLogInfo("[Begin] conversion to NetCDF of: " + metadataFile +"  "+ csvFile+"  "+ ncOutput)

        self.checkSource(metadataFile, csvFile)

        self.metadata = Metadata(metadataFile)
        self.metadataData = self.metadata.getMetadata()
        self.data = Data(csvFile)
        self.ncFile = Dataset(ncOutput, 'w', format='NETCDF4')
        # self.ncFile = Dataset(ncOutput, 'w', format='NETCDF3_CLASSIC')
        self.dimensions = self.metadata.getDimensions()
        self.globalAttributes = Metadata(metadataFile).getGlobalAttributes()
        self.globalAttributes.writeAttributes(self.ncFile)
        self.dimensions.writeDimensions(self.ncFile)
        self.variables = self.metadata.getVariables()
        self.writeVariablesData()
        Log().setLogInfo("[Finished] conversion to NetCDF of : "+ metadataFile + "  " + csvFile + "  " + ncOutput)

    def writeVariablesData(self):
        variables = self.metadataData['variables']
        variablesNames = ['_FillValue', 'variable_name', 'typeof', 'dim', 'value', 'csvcolumn']

        for variable in variables:
            variableCreated = self.variables.writeVariables(self.ncFile, variable)
            self.data.writeData(self.ncFile, variable, variableCreated)
            self.variables.deleteAttributes(variablesNames, variable)
            self.variables.addAttributeToVariable(variableCreated, variable)

    def checkSource(self, metadataFile, csvFile):
        if os.path.exists(metadataFile) == False:
            Log().setLogError('Not found .json file. (Metadata file)')
            Log().setLogInfo('The script has closed unsatisfactorily')
            sys.exit(-1)
        elif os.path.exists(csvFile):
            Log().setLogError('Not .csv / .data file. (Data file)')
            Log().setLogInfo('The script has closed unsatisfactorily')
            sys.exit(-1)

if __name__ == '__main__':
    NetCDFConverter('/Users/Loedded/Downloads/xx.json', '/Users/Loedded/Downloads/xx.dat',
                    '/Users/Loedded/Downloads/xx.nc')
