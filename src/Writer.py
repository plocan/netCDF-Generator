from Checker import Checker


class Writer(object):
    def __init__(self, data, dimensions, ncFile):
        self.data = data
        self.dimensions = dimensions
        self.ncFile = ncFile

    def write_variables_data(self, variables, variablesList, version):
        variablesNames = ['_FillValue', 'variable_name', 'typeof', 'dim', 'value', 'csvcolumn']

        for variable in variables:
            variableCreated = variablesList.write_variables(self.ncFile, variable, version)
            self.data.write_data(variable, variableCreated)
            variablesList.delete_attributes(variablesNames, variable)
            variablesList.add_attribute_to_variable(variableCreated, variable)

    def write_append_variables_data(self, variables):
        checker = Checker(self.data)
        checker.check_pos_time(self.dimensions.dimensionsList, variables, self.ncFile)
        checker.check_same_file(self.dimensions.dimensionsList, variables, self.ncFile)
        variables = variables.variablesList
        for variable in variables:
            if 'value' in variables[variable] and variables[variable]['value'] != "":
                continue
            dimension = variables[variable]['dim']
            appendPosition = checker.get_append_dictionary_element(dimension)
            appendMiddlePosition = checker.get_append_middle_dictionary_element(dimension)
            if appendPosition == 0 and appendMiddlePosition == 0:
                self.data.append_data(variables[variable], self.ncFile.variables[variable], self.dimensions)
            elif appendMiddlePosition > 0:
                self.data.append_data_in_the_middle(variables[variable], self.ncFile.variables[variable],
                                                    appendMiddlePosition, self.dimensions)
                continue
            else:
                self.data.append_data_to_file_with_old_data(variables[variable], self.ncFile.variables[variable],
                                                            appendPosition, self.dimensions)
