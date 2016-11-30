class Variables():
    def __init__(self, data):
        self.variablesList = {}
        for variable in data["variables"]:
            self.variablesList[variable["variable_name"]] = variable

    def getVariablesList(self):
        return self.variablesList.keys()

    def getVariableValueIterator(self, key):
        return self.variablesList[key].iteritems()
