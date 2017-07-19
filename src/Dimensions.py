import sys

from Log import Log

class Dimensions():

    def __init__(self, metadata):
        self.metadata = metadata
        self.dimensions = {}
        self.dimensionsList = []

    def set_dimensions_by_netcdf(self, dimensions):
        try:
            for dimension in dimensions:
                self.dimensions[dimension] = len(dimensions[dimension])
                self.dimensionsList.append(dimension)
        except:
            Log().set_log_error('Not found dimensions on .json file.')
            Log().set_log_info('The script has closed unsatisfactorily')
            sys.exit(-1)

    def write_dimensions(self, ncFile):
        try:
            dimensions = self.metadata['dimensions']
            for dimension in dimensions:
                if not dimension['length'] == "":
                    ncFile.createDimension(dimension['dimension_name'], dimension['length'])
        except:
            Log().set_log_warning('Error writing dimensions')
            Log().set_log_info('The script has closed unsatisfactorily')
            sys.exit(-1)

    def get_size_dimensions(self, dimension):
        return self.dimensions[dimension]

    def get_dimensions_list(self):
        return self.dimensionsList
