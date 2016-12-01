from src.inputData.Data import *
from src.inputData.Metadata import *


class NetCDFConverter(object):
    def __init__(self, metadataFile, csvFile, ncOutput):
        self.metadataFile = metadataFile
        Metadata(metadataFile)
        self.csvFile = csvFile
        self.ncOutput = ncOutput
        self.metadata = Metadata(self.metadataFile)
        self.data = Data(csvFile)


""""
if __name__ == '__main__':
    NetCDFConverter()

"""
