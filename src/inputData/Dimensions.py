import sys

from src.NetCDFConverter import NetCDFConverter
from src.inputData.Log import Log


class Dimensions():
    def __init__(self, metadata):
        self.dimensionsList = {}
        self.metadata = metadata
        self.createDimensionList()

    def createDimensionList(self):
        try:
            for dimension in self.metadata["dimensions"]:
                self.dimensionsList[dimension["dimension_name"]] = dimension["length"]
        except:
            Log().setLogError('Not found dimensions on .json file.')
            Log().setLogInfo('The script has closed unsatisfactorily')
            sys.exit(-1)

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
