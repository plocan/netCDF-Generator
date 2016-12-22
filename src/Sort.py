from src.Log import Log


class Sort(object):
    def __init__(self, header):
        self.header = header

    def sort_column(self, variable):
        if 'csvcolumn' in variable and variable['csvcolumn'] != "" and variable['csvcolumn'] in self.header:
            return 'csvcolumn'
        elif 'variable_name' in variable and variable['variable_name'] != "" and variable[
            'variable_name'] in self.header:
            return 'variable_name'
        elif 'standard_name' in variable and variable['standard_name'] != "" and variable[
            'standard_name '] in self.header:
            return 'standard_name'
        else:
            Log().set_log_warning(
                'NETCDF: Not found column for: ' + variable['variable_name'] + ' standard name: ' + variable[
                    'standard_name'])
