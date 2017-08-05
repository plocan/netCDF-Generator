import json

from Dimensions import Dimensions
from GlobalAttributes import GlobalAttributes
from Variables import Variables
from src.Variables_ego import Variables_ego


class Metadata(object):
    def __init__(self, sourceJson):
        with open(sourceJson) as data_file:
            self.data = json.load(data_file)
        self.globalAttributes = GlobalAttributes(self.data)
        self.dimensions = Dimensions(self.data)
        self.variables = Variables(self.data)
        self.variables_ego = Variables_ego(self.data)
        self.return_variable = 0
        data_file.close()

    def get_global_attributes(self):
        return self.globalAttributes

    def get_dimensions(self):
        return self.dimensions

    def get_variables(self):
        if self.return_variable == 0:
            return self.variables
        else:
            return self.variables_ego

    def get_metadata(self):
        return self.data

    def change_variable(self):
        self.return_variable = 1