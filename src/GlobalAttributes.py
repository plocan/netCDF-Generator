import sys
from datetime import datetime as dt

from Log import Log


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

    def writeAttributes(self, netCDF):
        try:
            for attribute in self.attributesList:
                if self.attributesList[attribute]:
                    setattr(netCDF, attribute, self.attributesList[attribute])

            netCDF.date_created = str(dt.now().date()) + 'T' + str(dt.now().time()) + 'Z'
        except:
            Log().setLogError('Error writing attributes')
            Log().setLogInfo('The script has closed unsatisfactorily')
            sys.exit(-1)


    def getNetCDFVersion(self):
        return self.attributesList["netcdf_version"]

    def getID(self):
        return self.attributesList["id"]
