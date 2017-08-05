from src.Log import Log


class Sort(object):
    def __init__(self, header):
        self.header = header

    def sort_column(self, variable):
        print variable
        if 'csvcolumn' in variable and variable['csvcolumn'] != "" and variable['csvcolumn'] in self.header:
            return 'csvcolumn'
        elif 'datacolumn' in variable and variable['datacolumn'] != "" and variable['datacolumn'] in self.header:
            return 'datacolumn'
        elif 'variable_name' in variable and variable['variable_name'] != "" and variable[
            'variable_name'] in self.header:
            return 'variable_name'
        elif 'standard_name' in variable and variable['standard_name'] != "" and variable[
            'standard_name'] in self.header:
            return 'standard_name'
        else:
            Log().set_log_warning(
                'NETCDF: Not found column for: ' + variable['variable_name'])
            return -1

