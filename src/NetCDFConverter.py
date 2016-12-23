import os

from netCDF4._netCDF4 import Dataset

from Data import *
from Log import Log
from Metadata import *
from Writer import Writer
from Checker import Checker


class NetCDFConverter(object):
    def __init__(self, metadataFile, csvFile, ncOutput):
        Log().set_log_info("[Begin] conversion to NetCDF of: " + metadataFile + "  " + csvFile + "  " + ncOutput)
        self.init_elements(metadataFile, csvFile, ncOutput)

        if not os.path.exists(self.ncOutput):
            try:
                self.ncFile = Dataset(self.ncOutput, 'w', format='NETCDF' + self.version)
            except:
                Log().set_log_error("The netCDF_version is wrong. Assigning the default value(netCDF4_CLASSIC) to "
                                    "netCDF_version")
                self.version = '4_CLASSIC'
                self.ncFile = Dataset(self.ncOutput, 'w', format='NETCDF' + self.version)

            self.globalAttributes = Metadata(metadataFile).get_global_attributes()
            self.globalAttributes.write_attributes(self.ncFile)
            self.dimensions.write_dimensions(self.ncFile)
            self.variables = self.metadata.get_variables()
            self.writer = Writer(self.data, self.dimensions, self.ncFile)
            self.writer.write_variables_data(self.metadataData['variables'], self.variables, self.version)
        else:  # Append start
            self.ncFile = Dataset(self.ncOutput, 'r+')
            self.dimensions.set_dimensions_by_netcdf(self.ncFile.dimensions)
            self.writer = Writer(self.data, self.dimensions, self.ncFile)
            self.writer.write_append_variables_data(self.metadata.get_variables())

        self.metadata.globalAttributes.max_min_attribute(self.ncFile)
        self.ncFile.close()
        Log().set_log_info("[Finished] conversion to NetCDF of : " + metadataFile + "  " + csvFile + "  " + ncOutput)

    def init_elements(self, metadataFile, csvFile, ncOutput):
        self.ncOutput = ncOutput
        self.ncOutput = Checker().check_source(metadataFile, csvFile, ncOutput)
        self.metadata = Metadata(metadataFile)
        self.metadataData = self.metadata.get_metadata()
        self.data = Data(csvFile)
        self.ncOutput = self.ncOutput + self.metadata.get_global_attributes().get_id() + ".nc"
        self.version = self.metadata.get_global_attributes().get_netcdf_version()
        self.temporalAppendPosition = {}
        self.dimensions = self.metadata.get_dimensions()

if __name__ == '__main__':
    NetCDFConverter('/Users/Loedded/Downloads/xx.json', '/Users/Loedded/Downloads/xx.dat', '/Users/Loedded/Downloads')

"""
if __name__ == '__main__':
    NetCDFConverter(sys.argv[1], sys.argv[2], sys.argv[3])
"""
