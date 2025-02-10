HEALPix Mapping Tutorial
====================

This tutorial demonstrates advanced usage of HEALPix mapping functionality in the Remote Sensing package.

Understanding HEALPix Resolution
-----------------------------

HEALPix divides the sphere into equal-area pixels. The resolution is controlled by the NSIDE parameter:

.. code-block:: python

   from remote_sensing.healpix import utils as hp_utils

   # Calculate NSIDE for different resolutions
   resolutions = [100, 50, 25, 10]  # km
   for res in resolutions:
       nside, pixel_size = hp_utils.get_nside_from_angular_size(res/111.1)
       print(f"{res:3d}km -> NSIDE={nside:4d}, actual pixel size={pixel_size*111.1:.1f}km")

Creating HEALPix Maps
------------------

There are several ways to create HEALPix maps:

From a Dataset
~~~~~~~~~~~~

.. code-block:: python

   from remote_sensing.rs_healpix import RS_Healpix

   # From a netCDF file
   hp_map = RS_Healpix.from_dataset_file(
       'data.nc',
       'temperature',
       resol_km=25
   )

From a DataArray
~~~~~~~~~~~~~

.. code-block:: python

   import xarray as xr
   import numpy as np

   # Create sample data
   lon = np.linspace(-180, 180, 360)
   lat = np.linspace(-90, 90, 180)
   data = np.random.rand(180, 360)

   # Create DataArray
   da = xr.DataArray(
       data,
       coords={'lat': lat, 'lon': lon},
       dims=['lat', 'lon']
   )

   # Convert to HEALPix
   hp_map = RS_Healpix.from_dataarray(da)

Combining Multiple Maps
-------------------

HEALPix maps can be combined in various ways:

Averaging Maps
~~~~~~~~~~~~

.. code-block:: python

   # Create list of maps
   maps = []
   for file in data_files:
       hp = RS_Healpix.from_dataset_file(file, 'temperature')
       maps.append(hp)

   # Average the maps
   mean_map = RS_Healpix.from_list(maps)

Filling Missing Data
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Fill missing data in one map using another
   primary_map = RS_Healpix.from_dataset_file('primary.nc', 'temperature')
   secondary_map = RS_Healpix.from_dataset_file('secondary.nc', 'temperature')

   # Fill gaps in primary map
   bbox = (-180, 180, -90, 90)  # whole globe
   primary_map.fill_in(secondary_map, bbox)

Advanced Operations
----------------

Working with Masked Data
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from remote_sensing.healpix import combine

   # Combine masked arrays
   combined = combine.average_masked_arrays([
       map1.hp,
       map2.hp,
       map3.hp
   ])

   # Create new map with combined data
   result_map = RS_Healpix(maps[0].nside)
   result_map.hp = combined

Regional Analysis
~~~~~~~~~~~~~~

.. code-block:: python

   # Define region
   bbox = (120, 140, 20