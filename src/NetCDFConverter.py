from netCDF4 import Dataset

from src.inputData.Data import *
from src.inputData.Metadata import *


class NetCDFConverter(object):
    def __init__(self, metadataFile, csvFile, ncOutput):
        # self.metadataFile = metadataFile
        # self.csvFile = csvFile
        # self.ncOutput = ncOutput
        self.metadata = Metadata(metadataFile)
        self.data = Data(csvFile)
        self.ncFile = Dataset(self.File, 'w', 'NETCDF4')
        self.globalAttributes = Metadata(metadataFile).getGlobalAttributes()
        self.globalAttributes.writeAttributes(self.ncFile)
        self.dimensions.writeDimensions(self.ncFile)
        self.variables.writeVariables(self.ncFile)

"""
if __name__ == '__main__':
    NetCDFConverter('/Users/Loedded/Downloads/xx.json', '/Users/Loedded/Downloads/xx.dat',
                    '/Users/Loedded/Downloads/xx.nc')
"""