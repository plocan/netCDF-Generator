from netCDF4 import Dataset

from src.inputData.Metadata import *


class NetCDFConverter(object):
    def __init__(self, metadataFile, csvFile, ncOutput):
        """self.metadataFile = metadataFile
        Metadata(metadataFile)
        self.csvFile = csvFile
        self.ncOutput = ncOutput
        self.metadata = Metadata(self.metadataFile)
        self.data = Data(csvFile)"""

        self.ncOutput = Dataset(ncOutput, 'w', 'NETCDF4')
        self.globalAttributes = Metadata(metadataFile).getGlobalAttributes()
        self.globalAttributes.writeAttributes(self.ncOutput)


if __name__ == '__main__':
    NetCDFConverter('/Users/Loedded/Downloads/xx.json', '/Users/Loedded/Downloads/xx.dat',
                    '/Users/Loedded/Downloads/xx.nc')
