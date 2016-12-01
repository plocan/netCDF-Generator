class Variables():
    def __init__(self, data):
        self.variablesList = {}
        for variable in data["variables"]:
            self.variablesList[variable["variable_name"]] = variable

    def getVariablesList(self):
        return self.variablesList.keys()

    def getVariableValueIterator(self, key):
        return self.variablesList[key].iteritems()
        
    def writeVariables(self, ncFile):
        variables = self.data['variables']
        varNames = ['_FillValue', 'variable_name', 'typeof', 'dim', 'value', 'csvcolumn']
        for var in variables:
            NcVar = self.createVariables(ncFile, var)
            #self.add_data(NcVar, var)
            #self.deleteatts(varNames, var)
            #self.add_atts(NcVar, var)

    def createVariables(self, ncFile, variable):
        fillVal = variable['_FillValue'] if '_FillValue' in variable and variable['_FillValue'] != "" else False
        if 'dim' in variable and variable['dim'] != "":
           ncVar = ncFile.createVariable(variable['variable_name'], variable['typeof'], (variable['dim']), fill_value=fillVal, zlib=True,complevel=9)
        else:
           ncVar = ncFile.createVariable(variable['variable_name'], variable['typeof'], fill_value=fillVal, zlib=True, complevel=9)
        return ncVar