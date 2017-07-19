import json

from Dimensions import Dimensions


class EgoReaderStandardMetadata(object):
    def __init__(self):
        self.dimensions = {}
        self.glider_characteristics_variables = {}
        self.glider_deployment_variables = {}
        with open("standar_data.json") as data_file:
            self.data = json.load(data_file)

        self.dimensions = Dimensions(self.data)
        for variable in self.data["glider_characteristics"]:
            self.glider_characteristics_variables[variable["variable_name"]] = variable

        for variable in self.data["glider_deployment"]:
            self.glider_deployment_variables[variable["variable_name"]] = variable

        data_file.close()

    def get_glider_characteristics_variables(self):
        return self.glider_characteristics_variables

    def get_dimensions(self):
        return self.dimensions

    def get_glider_deployment_variables(self):
        return self.glider_deployment_variables
