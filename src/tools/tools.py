from datetime import datetime

import numpy as np
from netCDF4 import date2num


def npind(nparray, elemt):
    itemindex = np.where(nparray == elemt)
    return (itemindex[0][0])


def date2days1950(date, dtformat, time_units):  # de un objeto datetime a dias desde 1950 que es lo q pide OceanSITES
    dati = datetime.strptime(date, dtformat)
    dateconverted = date2num(dati, units=time_units)
    return (dateconverted)


def fillarray(arraydata, totallen, fillvalue):
    i = len(arraydata)
    while i < totallen:
        arraydata = np.append(arraydata, fillvalue)
        i += 1
    return (arraydata)


def generatemdata(indexes, arraydata, lendimension1, lendimension2, fillvalue):
    i = 0
    while i < lendimension1:
        if i != 17:
            profarray = arraydata[indexes[i]:indexes[i + 1]]
        else:
            profarray = arraydata[indexes[i]:]
        profarray = fillarray(profarray, lendimension2, fillvalue)
        if i == 0:
            mat = np.matrix([profarray])
        else:
            mat = np.vstack([mat, profarray])
        i += 1
    return (mat)


def indexvar(var, data):
    i = 0
    res = -1
    for v in data:
        if var == v:
            res = i
        i = i + 1
    return res
