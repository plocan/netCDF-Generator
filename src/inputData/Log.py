import logging


class Log(object):
    def __init__(self):
        logging.basicConfig(filename='../log/netCDF-converter.log', level=logging.INFO,
                            format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    def setLogInfo(self, message):
        logging.info(message)

    def setLogWarning(self, message):
        logging.warning(message)

    def setLogError(self, message):
        logging.error(message)

    def setLogException(self, message):
        logging.exception(message)

    def setLogDebug(self, message):
        logging.debug(message)