class Dimensions():
    def __init__(self, data):
        self.dimensionsList = {}
        for dimension in data["dimensions"]:
            self.dimensionsList[dimension["dimension_name"]] = dimension["length"]

    def getDimensionsList(self):
        return self.dimensionsList.keys()

    def getDimensionValue(self, key):
        return self.dimensionsList[key]

    def getDimensionsListIterator(self):
        return self.dimensionsList.iteritems()
