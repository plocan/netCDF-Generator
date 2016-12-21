![Picture](http://empleo.plocan.eu/static/plocan.png)
# NetCDF-converter

## Table of contents

* [Introduction](#Introduction)
* [What does the code do?](#What does the code do?)
* [What the code doesn't do?](#What the code doesn't do?)
* [What could the code do in the future?](#What could the code do in the future?)
* [Prerequisites](#Prerequisites)
    * [Libraries](#Libraries)
    * [JSON Format](#JSON Format)
        * [OceanSites Standard](#OceanSites Standard)
        * [EgoGliders Standard](#EgoGliders Standard)
* [Version](#Version)
* [License](#License)
* [Download](#Download)
* [How-to use this code](#How-to use this code)
* [Authors](#Authors)


## Introduction

**NetCDF-Converter** is a file converter to *NetCDF* developed in python and that also complies with 
the standards of**OceanSites** and **EgoGliders** for *time series*

## What does the code do?

- Convert to NetCDF4.
- Convert to NetCDF3.
- You can add more data to a NetCDF document already created.


## What the code doesn't do?



## What could the code do in the future?



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

* To view the sample metadata file see [OceanSites JSON example](http://192.168.53.152/Data-Service/netCDF-convert/blob/master/osexample.json) file.

#### EgoGliders Standard v1.2


* For more information about the standard see [Data Format Reference Manual](http://archimer.ifremer.fr/doc/00239/34980/44905.pdf) file.

* To view the sample metadata file see [EgoGliders JSON example](http://192.168.53.152/Data-Service/netCDF-convert/blob/master/egexample.json) file.

## Version

Version 1.0

## License

* see [LICENSE](http://192.168.53.152/Data-Service/netCDF-convert/blob/master/LICENSE.md) file.

## Download

* [Version 1.0](http://192.168.53.152/Data-Service/netCDF-convert/repository/archive.zip?ref=master)[.zip]
* [Version 1.0](http://192.168.53.152/Data-Service/netCDF-convert/repository/archive.tar.gz?ref=master)[.tar.gz]
* [Version 1.0](http://192.168.53.152/Data-Service/netCDF-convert/repository/archive.tar.bz2?ref=master)[.tar.bz2]
* [Version 1.0](http://192.168.53.152/Data-Service/netCDF-convert/repository/archive.tar?ref=master)[.tar]


## How-to use this code


```
$ python NetCDFConverter.py parameter parameter destination

$ python NetCDFConverter.py /Users/user/Documents/example.json /Users/user/Documents/example.dat /Users/user/Documents
```


## Authors

* **Tania Morales** - *Team manager* - tania.morales@plocan.eu
* **Pablo Armas Matín** - *Developer* - pabloarmasm@gmail.com
* **Juan Carlos Arroyo Herrera** - *Developer* - jcah20022@gmail.com
* **Ismael Romero Rando** - *Developer* - ismael03011991@gmail.com

## Contact
#### PLOCAN (Plataforma Oceánica de Canarias)
* Homepage: http://plocan.eu/index.php/es/
* e-mail: 



