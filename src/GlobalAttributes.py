import sys
from datetime import datetime as dt

import numpy
from netCDF4._netCDF4 import num2date

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
        for attribute in self.attributesList:
            if self.attributesList[attribute]:
                setattr(netCDF, attribute, self.attributesList[attribute])

        netCDF.date_created = str(dt.now().date()) + 'T' + str(dt.now().time()) + 'Z'

    def get_netcdf_version(self):
        return self.attributesList["netcdf_version"]

    def get_id(self):
        return self.attributesList["id"]

    def max_min_attribute(self, netCDF):
        self.attributesList['geospatial_lat_max'] = numpy.amax(netCDF.variables['LATITUDE'][:])
        setattr(netCDF, 'geospatial_lat_max', self.attributesList['geospatial_lat_max'])
        self.attributesList['geospatial_lat_min'] = numpy.amin(netCDF.variables['LATITUDE'][:])
        setattr(netCDF, 'geospatial_lat_min', self.attributesList['geospatial_lat_min'])

        self.attributesList['geospatial_lon_max'] = numpy.amax(netCDF.variables['LONGITUDE'][:])
        setattr(netCDF, 'geospatial_lon_max', self.attributesList['geospatial_lon_max'])
        self.attributesList['geospatial_lon_min'] = numpy.amin(netCDF.variables['LONGITUDE'][:])
        setattr(netCDF, 'geospatial_lon_min', self.attributesList['geospatial_lon_min'])

        self.attributesList['geospatial_vertical_max'] = numpy.amax(netCDF.variables['DEPTH'][:])
        setattr(netCDF, 'geospatial_vertical_max', self.attributesList['geospatial_vertical_max'])
        self.attributesList['geospatial_vertical_min'] = numpy.amin(netCDF.variables['DEPTH'][:])
        setattr(netCDF, 'geospatial_vertical_min', self.attributesList['geospatial_vertical_min'])

        units = str(netCDF.variables['TIME'].units)
        if units.find("days") > -1:
            time_units = 'days since 1950-01-01T 00:00:00.0Z'
            time = str(num2date(numpy.amax(netCDF.variables['TIME'][:]), units=time_units))
            time = time[:10] + "T" + time[11:] + "Z"
            self.attributesList['time_coverage_end'] = time
            setattr(netCDF, 'time_coverage_end', self.attributesList['time_coverage_end'])
            time = str(num2date(numpy.amin(netCDF.variables['TIME'][:]), units=time_units))
            time = time[:10] + "T" + time[11:] + "Z"
            self.attributesList['time_coverage_start'] = time
            setattr(netCDF, 'time_coverage_start', self.attributesList['time_coverage_start'])
        elif units.find("seconds") > -1:
            time_units = 'seconds since 1970-01-01T00:00:00.0Z'
            time = str(num2date(numpy.amax(netCDF.variables['TIME'][:]), units=time_units))
            time = time[:10] + "T" + time[11:] + "Z"
            self.attributesList['time_coverage_end'] = time
            setattr(netCDF, 'time_coverage_end', self.attributesList['time_coverage_end'])
            time = str(num2date(numpy.amin(netCDF.variables['TIME'][:]), units=time_units))
            time = time[:10] + "T" + time[11:] + "Z"
            self.attributesList['time_coverage_start'] = time
            setattr(netCDF, 'time_coverage_start', self.attributesList['time_coverage_start'])

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
