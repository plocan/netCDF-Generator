from Checker import Checker
from Log import Log


class Variables():
    def __init__(self, metadata):
        self.variablesList = {}
        for variable in metadata["variables"]:
            self.variablesList[variable["variable_name"]] = variable

    def write_variables(self, ncFile, variable, version):
        return self.create_variables_for_netCDF(ncFile, variable)

    def create_variables_for_netCDF(self, ncFile, variable):
        fillVal = variable['_FillValue'] if '_FillValue' in variable and variable['_FillValue'] != "" else False
        dimension = Checker().check_dimensions(variable)
        if dimension != "":
            ncVariable = ncFile.createVariable(variable['variable_name'], variable['typeof'], (variable[dimension]),
                                               fill_value=float(fillVal), zlib=True, complevel=9)
        else:
            ncVariable = ncFile.createVariable(variable['variable_name'], variable['typeof'],
                                               fill_value=float(fillVal),
                                               zlib=True, complevel=9)
        return ncVariable

    def add_attribute_to_variable(self, variable, attributes):
        try:
            for attribute in attributes:
                if attributes[attribute]:
                    setattr(variable, attribute, attributes[attribute])
        except:
            Log().set_log_warning('Error adding attribute')

    def delete_attributes(self, variablesName, variable):
        try:
            for key in variablesName:
                if key in variable:
                    del variable[key]
        except:
            Log().set_log_warning('Error deleting attribute')
