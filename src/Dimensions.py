class Dimensions():

    def __init__(self, metadata):
        self.metadata = metadata
        self.dimensions = {}
        self.dimensionsList = []

    def set_dimensions_by_netcdf(self, dimensions):
        for dimension in dimensions:
            self.dimensions[dimension] = len(dimensions[dimension])
            self.dimensionsList.append(dimension)

    def write_dimensions(self, ncFile):
        dimensions = self.metadata['dimensions']
        for dimension in dimensions:
            ncFile.createDimension(dimension['dimension_name'], dimension['length'])

    def get_size_dimensions(self, dimension):
        return self.dimensions[dimension]

    def get_dimensions_list(self):
        return self.dimensionsList
