class Dimensions():
    def __init__(self, data):
        self.dimensionsList = {}
        self.createDimensionList(data)

    def createDimensionList(self, data):
        for dimension in data["dimensions"]:
            self.dimensionsList[dimension["dimension_name"]] = dimension["length"]

    def getDimensionsList(self):
        return self.dimensionsList.keys()

    def getDimensionValue(self, key):
        return self.dimensionsList[key]

    def getDimensionsListIterator(self):
        return self.dimensionsList.iteritems()

    def writeDimensions(self, ncFile):
        dimensions = self.data['dimensions']
        for dimension in dimensions:
            ncFile.createDimension(dimension['dimension_name'], dimension['length'])
