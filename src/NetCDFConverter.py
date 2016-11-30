from inputData import Metadata


class NCFile(object):
    def __init__(self, metadateFile, csvFile, ncOutput):
        self.metadataFile = metadateFile
        self.csvFile = csvFile
        self.ncOutput = ncOutput
        self.metadata = Metadata(self.metadataFile)
