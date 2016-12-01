class Dimensions():
    def __init__(self, metadata):
        self.dimensionsList = {}
        self.metadata = metadata
        self.createDimensionList()

    def createDimensionList(self):
        for dimension in self.metadata["dimensions"]:
            self.dimensionsList[dimension["dimension_name"]] = dimension["length"]

    def getDimensionsList(self):
        return self.dimensionsList.keys()

    def getDimensionValue(self, key):
        return self.dimensionsList[key]

    def getDimensionsListIterator(self):
        return self.dimensionsList.iteritems()

    def writeDimensions(self, ncFile):
        dimensions = self.metadata['dimensions']
        for dimension in dimensions:
            ncFile.createDimension(dimension['dimension_name'], dimension['length'])
