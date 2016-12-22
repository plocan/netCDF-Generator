import os
import sys

from netCDF4._netCDF4 import Dataset

from Data import *
from Log import Log
from Metadata import *
from Writer import Writer


class NetCDFConverter(object):
    def __init__(self, metadataFile, csvFile, ncOutput):
        Log().set_log_info("[Begin] conversion to NetCDF of: " + metadataFile + "  " + csvFile + "  " + ncOutput)
        self.ncOutput = ncOutput
        self.check_source(metadataFile, csvFile)
        self.metadata = Metadata(metadataFile)
        self.metadataData = self.metadata.get_metadata()
        self.data = Data(csvFile)
        self.ncOutput = self.ncOutput + self.metadata.get_global_attributes().get_id() + ".nc"
        self.version = self.metadata.get_global_attributes().get_netcdf_version().replace(" ", "_")
        self.temporalAppendPosition = {}

        if not os.path.exists(self.ncOutput):
            self.ncFile = Dataset(self.ncOutput, 'w', format='NETCDF' + self.version)
            self.dimensions = self.metadata.get_dimensions()
            self.globalAttributes = Metadata(metadataFile).get_global_attributes()
            self.globalAttributes.write_attributes(self.ncFile)
            self.dimensions.write_dimensions(self.ncFile)
            self.variables = self.metadata.get_variables()
            self.writer = Writer(self.data, self.dimensions, self.ncFile)
            self.writer.write_variables_data(self.metadataData['variables'], self.variables, self.version)
        else:
            self.ncFile = Dataset(self.ncOutput, 'r+')
            self.dimensions = self.metadata.get_dimensions()
            self.dimensions.set_dimensions_by_netcdf(self.ncFile.dimensions)
            self.writer = Writer(self.data, self.dimensions, self.ncFile)
            self.writer.write_append_variables_data(self.metadata.get_variables())

        self.metadata.globalAttributes.max_min_attribute(self.ncFile)

        Log().set_log_info("[Finished] conversion to NetCDF of : " + metadataFile + "  " + csvFile + "  " + ncOutput)

    def check_source(self, metadataFile, csvFile):
        if not os.path.exists(metadataFile):
            Log().set_log_error('Not found .json file. (Metadata file)')
            Log().set_log_info('The script has closed unsatisfactorily')
            sys.exit(-1)
        elif not os.path.exists(csvFile):
            Log().set_log_error('Not .csv / .data file. (Data file)')
            Log().set_log_info('The script has closed unsatisfactorily')
            sys.exit(-1)
        finalCharacter = self.ncOutput[len(self.ncOutput) - 1]
        if finalCharacter != '/':
            self.ncOutput += '/'



if __name__ == '__main__':
    NetCDFConverter('/Users/Loedded/Downloads/xx.json', '/Users/Loedded/Downloads/xx.dat', '/Users/Loedded/Downloads')

"""
if __name__ == '__main__':
    NetCDFConverter(sys.argv[1], sys.argv[2], sys.argv[3])
"""
