from src.inputData.Log import Log


class ColumnSeacher(object):

        def __init__(self):
            self.nameColumns = ['value', 'csvcolumn', 'variable_name', 'standard_name']
            pass

        def searchColumn(self, variable):
            for name in self.nameColumns:
                if name in variable and variable[name] != "":
                    return name


            Log().setLogWarning('NETCDF: Not found column for: ' + variable['variable_name'] + ' standard name: ' + variable['standard_name'])