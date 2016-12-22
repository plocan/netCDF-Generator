class Dimensions():

    def __init__(self, metadata):
        self.metadata = metadata
        self.dimensions = {}
        self.dimensionsList = []

    def setDimensionsByNetCDF(self, dimensions):
        for dimension in dimensions:
            self.dimensions[dimension] = len(dimensions[dimension])
            self.dimensionsList.append(dimension)

    def writeDimensions(self, ncFile):
        dimensions = self.metadata['dimensions']
        for dimension in dimensions:
            ncFile.createDimension(dimension['dimension_name'], dimension['length'])

    def getSizeDimensions(self, dimension):
        return self.dimensions[dimension]

    def getDimensionsList(self):
        return self.dimensionsList
