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

    def get_global_attributes(self):
        return self.globalAttributes

    def get_dimensions(self):
        return self.dimensions

    def get_variables(self):
        return self.variables

    def get_metadata(self):
        return self.data
