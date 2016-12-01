from netCDF4 import Dataset

from src.inputData.Data import *
from src.inputData.Metadata import *


class NetCDFConverter(object):
    def __init__(self, metadataFile, csvFile, ncOutput):
        # self.metadataFile = metadataFile
        # self.csvFile = csvFile
        # self.ncOutput = ncOutput
        self.metadata = Metadata(metadataFile)
        self.metadataData = self.metadata.getMetadata()
        self.data = Data(csvFile)
        self.ncFile = Dataset(ncOutput, 'w', 'NETCDF4')
        self.dimensions = self.metadata.getDimensions()
        self.globalAttributes = Metadata(metadataFile).getGlobalAttributes()
        self.globalAttributes.writeAttributes(self.ncFile)
        self.dimensions.writeDimensions(self.ncFile)
        self.variables = self.metadata.getVariables()
        self.writeVariablesData()

    def writeVariablesData(self):
        variables = self.metadataData['variables']
        variablesNames = ['_FillValue', 'variable_name', 'typeof', 'dim', 'value', 'csvcolumn']

        for variable in variables:
            variableCreated = self.variables.writeVariables(self.ncFile, variable)
            self.data.writeData(self.ncFile, variable, variableCreated)
            self.variables.deleteAttributes(variablesNames, variable)
            self.variables.addAttributeToVariable(variableCreated, variable)


if __name__ == '__main__':
    NetCDFConverter('/Users/Loedded/Downloads/xx.json', '/Users/Loedded/Downloads/xx.dat',
                    '/Users/Loedded/Downloads/xx.nc')
