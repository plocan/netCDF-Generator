from Checker import Checker


class Writer(object):
    def __init__(self, data, dimensions, ncFile):
        self.data = data
        self.dimensions = dimensions
        self.ncFile = ncFile

    def writeVariablesData(self, variables, variablesList, version):
        variablesNames = ['_FillValue', 'variable_name', 'typeof', 'dim', 'value', 'csvcolumn']

        for variable in variables:
            variableCreated = variablesList.writeVariables(self.ncFile, variable, version)
            self.data.writeData(variable, variableCreated)
            variablesList.deleteAttributes(variablesNames, variable)
            variablesList.addAttributeToVariable(variableCreated, variable)

    def writeAppendVariablesData(self, variables):
        checker = Checker(self.data)
        checker.checkPosTime(self.dimensions.dimensionsList, variables, self.ncFile)
        checker.checkSameFile(self.dimensions.dimensionsList, variables, self.ncFile)
        variables = variables.variablesList
        for variable in variables:
            if 'value' in variables[variable] and variables[variable]['value'] != "":
                continue
            dimension = variables[variable]['dim']
            appendPosition = checker.getAppendDictionaryElement(dimension)
            appendMiddlePosition = checker.getAppendMiddleDictionaryElement(dimension)
            if appendPosition == 0 and appendMiddlePosition == 0:
                self.data.appendData(variables[variable], self.ncFile.variables[variable], self.dimensions)
            elif appendMiddlePosition > 0:
                self.data.appendDataInTheMiddle(variables[variable], self.ncFile.variables[variable],
                                                appendMiddlePosition, self.dimensions)
                continue
            else:
                self.data.appendDataToFileWithOldData(variables[variable], self.ncFile.variables[variable],
                                                      appendPosition, self.dimensions)
