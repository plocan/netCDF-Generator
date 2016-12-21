import sys

from src.Log import Log


class Variables():
    def __init__(self, metadata):
        self.variablesList = {}
        for variable in metadata["variables"]:
            self.variablesList[variable["variable_name"]] = variable

    def writeVariables(self, ncFile, variable, version):
        return self.createVariablesForNetCDF(ncFile, variable)

    def createVariablesForNetCDF(self, ncFile, variable):
        fillVal = variable['_FillValue'] if '_FillValue' in variable and variable['_FillValue'] != "" else False
        if 'dim' in variable and variable['dim'] != "":
            ncVariable = ncFile.createVariable(variable['variable_name'], variable['typeof'], (variable['dim']),
                                               fill_value=float(fillVal), zlib=True, complevel=9)
        else:
            ncVariable = ncFile.createVariable(variable['variable_name'], variable['typeof'],
                                               fill_value=float(fillVal),
                                               zlib=True, complevel=9)
        return ncVariable

    def addAttributeToVariable(self, variable, attributes):
        try:
            for attribute in attributes:
                if attributes[attribute]:
                    setattr(variable, attribute, attributes[attribute])
        except:
            Log().setLogWarning('Error adding attribute')

    def deleteAttributes(self, variablesName, variable):
        try:
            for key in variablesName:
                if key in variable:
                    del variable[key]
        except:
            Log().setLogWarning('Error deleting attribute')