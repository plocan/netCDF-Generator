![Picture](https://plocan.eu/wp-content/uploads/PLOC_logo.svg)
# NetCDF-Generator

## Table of contents

* Introduction
* What does the code do?
* What the code doesn't do?
* What could the code do in the future?
* Prerequisites
    * Libraries
    * JSON Format
        * OceanSites Standard
        * EgoGliders Standard
* Version
* License
* Download
* How-to use this code
* Authors


## Introduction

The **netCDF-Generator** is a software developed in python that generates netCDF documents 
complying the **OceanSites** standard and the **EgoGliders** standard for *time series*. 

## What does the code do?

- Convert to netCDF4 and netCDF4_CLASSIC.
- Convert to netCDF3 and his variants.
- You can add new data to a netCDF document already created considering the following cases:
    - If you have a new CSV file with new ordered by time data.
    - If you have a new CSV file with new messy by time data.
    - If you have the same CSV file with more data than before.
- You can put the netCDF version in JSON as a number considering the following cases:
    - If you put 3.5, the version will be netCDF3_CLASSIC.
    - If you put 3.6 and, the version will be netCDF3_64BIT_OFFSET.
    - If you put 4 or if you don't put any value, the version would be netCDF4_CLASSIC.
- You can put the netCDF version in JSON as a string considering these cases:
    - You can put the string in lowercase as in the following example 3_classic.
    - You can put spaces as in the following example 3 64BIT OFFSET.
    - You should write the correct name as in the following example 3_CLASSIC.

## What the code doesn't do?
- The JSON file and the CSV file must be in utf-8 and shouldn't have any character 
outside English alphabet. For example: º, ò, í, etc.
- If you put a different name than standard names you will have to use that name 
in the JSON DataColumn attribute of the variable.
-This software has support for log, but for the use, it's necessary upgrade to root for his use.


## What could the code do in the future?
- The software could get the data from a database.
- The software could generate a future version of netCDF.
- The software could comply new versions of the actual standards or others.
- The software could have an user interface for your personal use.
- The software could read profiles and grid data.


## Prerequisites

[Python 2.7](https://www.python.org/download/releases/2.7/)

### Libraries

- [NetCDF4](https://pypi.python.org/pypi/netCDF4) v1.2.6  
- [HDF5](http://www.h5py.org/) v2.6.0
- [Libcurl](https://curl.haxx.se/libcurl/) v0.7.12
- [Numpy](http://www.numpy.org/) v1.12.Orc1
- [Pandas](http://pandas.pydata.org/) v0.19.1

### JSON Format

#### OceanSites Standard v1.3


* For more information about the standard see [Data Format Reference Manual](http://www.oceansites.org/docs/oceansites_data_format_reference_manual.pdf) file.

* To view the sample metadata file see [OceanSites JSON example](https://github.com/plocan/netCDF-Generator/blob/master/docs/osexample.json) file.

#### EgoGliders Standard v1.2


* For more information about the standard see [Data Format Reference Manual](http://archimer.ifremer.fr/doc/00239/34980/44905.pdf) file.

* To view the sample metadata file see [EgoGliders JSON example](https://github.com/plocan/netCDF-Generator/blob/master/docs/egexample.json) file.

## Version

Version 1.0

## License

* See [LICENSE](https://github.com/plocan/netCDF-Generator/blob/master/LICENSE.md) file.

## Download

* [Version 1.0](https://github.com/plocan/netCDF-Generator/archive/master.zip)[.zip]
* [Version 1.0](https://github.com/plocan/netCDF-Generator/archive/master.tar.gz)[.tar.gz]
* [Version 1.0](https://github.com/plocan/netCDF-Generator/archive/master.tar.bz2)[.tar.bz2]
* [Version 1.0](https://github.com/plocan/netCDF-Generator/archive/master.tar)[.tar]


## How-to use this code


```
$ python NetCDFConverter.py parameter parameter destination

$ python NetCDFConverter.py /Users/user/Documents/example.json /Users/user/Documents/example.dat /Users/user/Documents
```


## Authors

* **Tania Morales** - *Team manager* - tania.morales@plocan.eu

OceanSite developers:
* **Pablo Armas Matín** - *Developer* - pabloarmasm@gmail.com - GitHub: **PabloArmasM**
* **Juan Carlos Arroyo Herrera** - *Developer* - jcah20022@gmail.com - GitHub: **bultrifacio**
* **Ismael Romero Rando** - *Developer* - ismael03011991@gmail.com

EgoGlider developer:
* **Pablo Armas Matín** - *Developer* - pabloarmasm@gmail.com - GitHub: **PabloArmasM**

## Contact
#### PLOCAN (Plataforma Oceánica de Canarias)
* Homepage: http://plocan.eu/index.php/es/
* e-mail: areatic@plocan.eu



