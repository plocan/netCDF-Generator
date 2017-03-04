import os

from netCDF4._netCDF4 import Dataset

from Data import *
from Log import Log
from Metadata import *
from Writer import Writer
from Checker import Checker
from EgoReaderStandardMetadata import EgoReaderStandardMetadata


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
            self.create_netcdf()
        else:  # Append start
            self.ncFile = Dataset(self.ncOutput, 'r+')
            self.append_netcdf()
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
        self.globalAttributes = Metadata(metadataFile).get_global_attributes()
        self.naming_authority = self.globalAttributes.attributesList['naming_authority']

        if self.naming_authority == 'EGO':
            self.ego_standard_metadata = EgoReaderStandardMetadata()
            self.dimensions = self.ego_standard_metadata.get_dimensions()
        else:
            self.dimensions = self.metadata.get_dimensions()




    def create_netcdf(self):
        self.globalAttributes.write_attributes(self.ncFile)
        if self.naming_authority == 'EGO':
            self.dimensions.write_dimensions(self.ncFile)

            self.variables = self.metadata.get_variables()
            self.writer = Writer(self.data, self.dimensions, self.ncFile)
            self.writer.write_variables_data(self.metadataData['variables'], self.variables, self.version)

            self.variables = self.ego_standard_metadata.get_glider_characteristics_variables()
            self.writer = Writer(self.data, self.dimensions, self.ncFile)
            self.writer.write_variables_data(self.metadataData['variables'], self.variables, self.version)

            self.variables = self.ego_standard_metadata.get_glider_deployment_variables()
            self.writer = Writer(self.data, self.dimensions, self.ncFile)
            self.writer.write_variables_data(self.metadataData['variables'], self.variables, self.version)

        else:
            self.dimensions.write_dimensions(self.ncFile)
            self.variables = self.metadata.get_variables()
            self.writer = Writer(self.data, self.dimensions, self.ncFile)
            self.writer.write_variables_data(self.metadataData['variables'], self.variables, self.version)

    def append_netcdf(self):
        self.dimensions.set_dimensions_by_netcdf(self.ncFile.dimensions)
        self.writer = Writer(self.data, self.dimensions, self.ncFile)
        self.writer.write_append_variables_data(self.metadata.get_variables())
"""
if __name__ == '__main__':
    NetCDFConverter(sys.argv[1], sys.argv[2], sys.argv[3])
"""
if __name__ == '__main__':
    NetCDFConverter("/Users/Loedded/Desktop/EgoGliders/EGO_nc_v1.json","/Users/Loedded/Desktop/EgoGliders/p201_ESTOC_2015_2.csv","/Users/Loedded/Downloads")
