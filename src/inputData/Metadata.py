import json

import Dimensions
import GlobalAttributes
import Variables


class Metadata():
    def __init__(self, source):
        with open(source) as data_file:
            data = json.load(data_file)

        self.globalAttributes = GlobalAttributes(data)
        self.dimensions = Dimensions(data)
        self.variables = Variables(data)
        data_file.close()

    def getGlobalAttributes(self):
        return self.globalAttributes

    def getDimensions(self):
        return self.dimensions

    def getVariables(self):
        return self.variables


"""source = 'test.json'
testMetadata = metadata(source)


my_global_attributes = testMetadata.getGlobalAttributes()
print "\n getAttributesList"
print my_global_attributes.getAttributesList()

print "\n getAttributeValue"
for key in my_global_attributes.getAttributesList():
    print key + ": " + my_global_attributes.getAttributeValue(key)

print "\n getAttributesListIterator"
for key, value in my_global_attributes.getAttributesListIterator():
    print key + ": " + value


my_dimensions = testMetadata.getDimensions()
print "\n getDimensionsList"
print my_dimensions.getDimensionsList()

print "\n getDimensionValue"
for key in my_dimensions.getDimensionsList():
    print key + ": "
    print my_dimensions.getDimensionValue(key)

print "\n getDimensionsListIterator"
for key, value in my_dimensions.getDimensionsListIterator():
    print key + ": "
    print value


my_variables = testMetadata.getVariables()
print "\n getVariablesList"
print my_variables.getVariablesList()

print "\n getVariableValueIterator"
for key in my_variables.getVariablesList():
    print "\n" + key
    for key, value in my_variables.getVariableValueIterator(key):
        print key + ": "
        print value
"""
