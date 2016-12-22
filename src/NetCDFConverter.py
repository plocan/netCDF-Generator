import os
import sys

from netCDF4._netCDF4 import Dataset

from Data import *
from Log import Log
from Metadata import *
from Writer import Writer


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
        self.temporalAppendPosition = {}

        if not os.path.exists(self.ncOutput):
            self.ncFile = Dataset(self.ncOutput, 'w', format='NETCDF' + self.version)
            self.dimensions = self.metadata.getDimensions()
            self.globalAttributes = Metadata(metadataFile).getGlobalAttributes()
            self.globalAttributes.writeAttributes(self.ncFile)
            self.dimensions.writeDimensions(self.ncFile)
            self.variables = self.metadata.getVariables()
            self.writer = Writer(self.data, self.dimensions, self.ncFile)
            self.writer.writeVariablesData(self.metadataData['variables'], self.variables, self.version)
        else:
            self.ncFile = Dataset(self.ncOutput, 'r+')
            self.dimensions = self.metadata.getDimensions()
            self.dimensions.setDimensionsByNetCDF(self.ncFile.dimensions)
            self.writer = Writer(self.data, self.dimensions, self.ncFile)
            self.writer.writeAppendVariablesData(self.metadata.getVariables())

        self.metadata.globalAttributes.max_min_attribute(self.ncFile)

        Log().setLogInfo("[Finished] conversion to NetCDF of : " + metadataFile + "  " + csvFile + "  " + ncOutput)

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



if __name__ == '__main__':
    NetCDFConverter('/Users/Loedded/Downloads/xx.json', '/Users/Loedded/Downloads/xx.dat', '/Users/Loedded/Downloads')
