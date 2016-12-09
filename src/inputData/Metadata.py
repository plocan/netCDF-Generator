import json

from Dimensions import Dimensions
from GlobalAttributes import GlobalAttributes
from Variables import Variables


class Metadata(object):
    def __init__(self, sourceJson):
        with open(sourceJson) as data_file:
            self.data = json.load(data_file)
        self.globalAttributes = GlobalAttributes(self.data)
        self.dimensions = Dimensions(self.data)
        self.variables = Variables(self.data)
        data_file.close()

    def getGlobalAttributes(self):
        return self.globalAttributes

    def getDimensions(self):
        return self.dimensions

    def getVariables(self):
        return self.variables

    def getMetadata(self):
        return self.data
