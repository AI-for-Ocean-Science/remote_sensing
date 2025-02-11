.. highlight:: rest

******************
View NetCDF Script
******************

The Remote Sensing package includes a script to view NetCDF files. 
The script inputs a NetCDF file and the data
variable and displays the data in a plot on the globe.

Main arguments
==============

- ``netcdf_file``: File+path to NetCDF file
- ``variable``: Variable to view (or a 'shortcut', e.g. sst)

Optional arguments
==================

- ``--lat_min``: Minimum latitude
- ``--lat_max``: Maximum latitude
- ``--lon_min``: Minimum longitude
- ``--lon_max``: Maximum longitude
- ``--projection``: Projection for the plot; (mollweide, platecarree)
- ``--ssize``: Size of the points

Usage
=====

.. code-block:: bash

    usage: rs_view_nc [-h] [--lat_min LAT_MIN] [--lat_max LAT_MAX] [--lon_min LON_MIN]
                      [--lon_max LON_MAX] [--projection PROJECTION] [--ssize SSIZE]
                      [--cmap CMAP] [--itime ITIME]
                      netcdf_file variable

    View a variable in a NetCDF file

    positional arguments:
      netcdf_file           File+path to NetCDF file
      variable              Variable to view (or a 'shortcut', e.g. sst)

    options:
      -h, --help            show this help message and exit
      --lat_min LAT_MIN     Minimum latitude
      --lat_max LAT_MAX     Maximum latitude
      --lon_min LON_MIN     Minimum longitude
      --lon_max LON_MAX     Maximum longitude
      --projection PROJECTION
                            Projection for the plot; (mollweide, platecarree)
      --ssize SSIZE         Size of the points
      --cmap CMAP           Color map
      --itime ITIME         Time index to view, if applicable
