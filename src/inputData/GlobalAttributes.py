import re
from datetime import datetime as dt

class GlobalAttributes():
    def __init__(self, data):
        self.data = data
        self.attributesList = {}
        self.createAttributeList()

    def createAttributeList(self):
        try:
            for key, value in self.data["global_attributes"].items():
                self.attributesList[key] = value
        except:
            Log().setLogError('Not found global_attributes on .json file.')
            Log().setLogInfo('The script has closed unsatisfactorily')
            sys.exit(-1)

    def getAttributesList(self):
        return self.attributesList.keys()

    def getAttributeValue(self, key):
        return self.attributesList[key]

    def getAttributesListIterator(self):
        return self.attributesList.iteritems()

    def writeAttributes(self, netCDF):
        for attribute in self.attributesList:
            if self.attributesList[attribute]:
                setattr(netCDF, attribute, self.attributesList[attribute])

        netCDF.date_created = str(dt.now().date()) + 'T' + str(dt.now().time()) + 'Z'

    def getNetCDFVersion(self):
        return re.sub("\D", "", self.attributesList["netcdf_version"])
