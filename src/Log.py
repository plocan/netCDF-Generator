import logging


class Log(object):
    def __init__(self):
        logging.basicConfig(filename='../log/netCDF-converter.log', level=logging.INFO,
                            format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y/%m/%d %S:%I:%M %p')

    def set_log_info(self, message):
        logging.info(message)

    def set_log_warning(self, message):
        logging.warning(message)

    def set_log_error(self, message):
        logging.error(message)

    def set_log_exception(self, message):
        logging.exception(message)

    def set_log_dSebug(self, message):
        logging.debug(message)
