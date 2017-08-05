from Checker import Checker
from Log import Log


class Variables_ego():
    def __init__(self, metadata):
        self.first = True
        self.variablesList = {}
        for variable in metadata["variables"]:
            self.variablesList[variable["variable_name"]] = variable

    def write_variables(self, ncFile, variable, version, data):
        return self.create_variables_for_netCDF(ncFile, variable, data)

    def create_variables_for_netCDF(self, ncFile, variable, data):
        fillVal = variable['_FillValue'] if '_FillValue' in variable and variable['_FillValue'] != "" else False
        dimension = Checker().check_dimensions(variable)
        if dimension != "":
            print "No dimension"
            if self.first:
                columns = data.get_column()
                row = data.get_row()
                ncFile.createDimension("columns", columns)
                ncFile.createDimension("row", row)
                self.first = False
            ncVariable = ncFile.createVariable(variable['variable_name'], variable['typeof'], dimensions=("columns", "row"),
                                               fill_value=float(fillVal), zlib=True, complevel=9)
        else:
            print "Si dimension"
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
