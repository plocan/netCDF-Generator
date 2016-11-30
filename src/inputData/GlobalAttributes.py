class GlobalAttributes():
    def __init__(self, data):
        self.attributesList = {}
        for key, value in data["global_attributes"].items():
            self.attributesList[key] = value

    def getAttributesList(self):
        return self.attributesList.keys()

    def getAttributeValue(self, key):
        return self.attributesList[key]

    def getAttributesListIterator(self):
        return self.attributesList.iteritems()
