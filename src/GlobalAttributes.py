import sys

import numpy
from netCDF4._netCDF4 import num2date
from datetime import datetime as datetime
from Log import Log


class GlobalAttributes():
    def __init__(self, data):
        self.data = data
        self.attributesList = {}
        self.create_attribute_list()

    def create_attribute_list(self):
        try:
            for key, value in self.data["global_attributes"].items():
                self.attributesList[key] = value
        except:
            Log().set_log_error('Not found global_attributes on .json file.')
            Log().set_log_info('The script has closed unsatisfactorily')
            sys.exit(-1)

    def write_attributes(self, netCDF):
        try:
            for attribute in self.attributesList:
                if self.attributesList[attribute]:
                    setattr(netCDF, attribute, self.attributesList[attribute])
            netCDF.date_created = str(datetime.now().date()) + 'T' + str(datetime.now().time()) + 'Z'
        except:
            Log().set_log_error('Error writing attributes')
            Log().set_log_info('The script has closed unsatisfactorily')
            sys.exit(-1)

    def get_id(self):
        return self.attributesList["id"]

    def max_min_attribute(self, netCDF):

        self.set_global_attribute(netCDF, 'geospatial_lat_max', 'geospatial_lat_min', 'LATITUDE')
        self.set_global_attribute(netCDF, 'geospatial_lon_max', 'geospatial_lon_min', 'LONGITUDE')
        self.set_global_attribute(netCDF, 'geospatial_vertical_max', 'geospatial_vertical_min', 'DEPTH')

        units = str(netCDF.variables['TIME'].units)
        if units.find("days") > -1:
            time_units = 'days since 1950-01-01T 00:00:00.0Z'
            self.set_time_global_attribute(netCDF, 'time_coverage_end', 'time_coverage_start', 'TIME', time_units)
        elif units.find("seconds") > -1:
            time_units = 'seconds since 1970-01-01T00:00:00.0Z'
            self.set_time_global_attribute(netCDF, 'time_coverage_end', 'time_coverage_start', 'TIME', time_units)

    def set_global_attribute(self, netCDF, keymax, keymin, value):
        try:
            self.attributesList[keymax] = numpy.amax(netCDF.variables[value][:])
            setattr(netCDF, keymax, self.attributesList[keymax])
            self.attributesList[keymin] = numpy.amin(netCDF.variables[value][:])
            setattr(netCDF, keymin, self.attributesList[keymin])
        except:
            Log().set_log_warning('Error creating global attribute')


    def set_time_global_attribute(self, netCDF, keymax, keymin, value, format):
        try:
            time = str(num2date(numpy.amax(netCDF.variables[value][:]), units=format))
            time = time[:10] + "T" + time[11:] + "Z"
            self.attributesList[keymax] = time
            setattr(netCDF, keymax, self.attributesList[keymax])
            time = str(num2date(numpy.amin(netCDF.variables[value][:]), units=format))
            time = time[:10] + "T" + time[11:] + "Z"
            self.attributesList[keymin] = time
            setattr(netCDF, keymin, self.attributesList[keymin])
        except:
            Log().set_log_warning('Error creating global attribute')

    def get_netcdf_version(self):
        self.version = self.attributesList["netcdf_version"]
        if self.version == '3.5':
            self.version = '3_CLASSIC'
        elif self.version == '3.6':
            self.version = '3_64BIT_OFFSET'
        elif self.version == '':
            self.version = '4_CLASSIC'
        else:
            self.version = self.version.upper().replace(" ", "_")
        return self.version
