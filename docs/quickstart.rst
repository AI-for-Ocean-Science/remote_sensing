Quickstart Guide
==============

This guide will help you get started with the Remote Sensing package.

Basic Usage
----------

Downloading SST Data
~~~~~~~~~~~~~~~~~~

Download recent AMSR2 data for a specific region:

.. code-block:: python

   from remote_sensing.download import podaac

   # Get data for the past day
   files, checksums = podaac.grab_file_list(
       'AMSR2-REMSS-L2P_RT-v8.2',
       dt_past={'days': 1},
       bbox='127,18,134,23'  # lon_min,lat_min,lon_max,lat_max
   )

   # Download the files
   podaac.download_files(files)

Loading and Processing SST Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Load and process SST data from a NetCDF file:

.. code-block:: python

   from remote_sensing import sst

   # Load SST data
   sst_data, quality, lat, lon, time = sst.load('sst_file.nc')

   # Apply quality control
   from remote_sensing.netcdf import utils as nc_utils
   mask = nc_utils.build_mask(sst_data, quality, qual_thresh=5)

Creating HEALPix Maps
~~~~~~~~~~~~~~~~~~

Convert SST data to HEALPix format:

.. code-block:: python

   from remote_sensing.rs_healpix import RS_Healpix

   # Create HEALPix map from dataset
   healpix_map = RS_Healpix.from_dataset_file(
       'sst_file.nc',
       'sea_surface_temperature',
       resol_km=25  # spatial resolution
   )

   # Access HEALPix properties
   print(f"Resolution: {healpix_map.pix_resol} degrees")
   print(f"Pixel area: {healpix_map.pix_area} square degrees")

Visualization
-----------

Create a global map visualization:

.. code-block:: python

   # Plot HEALPix map
   healpix_map.plot(
       vmin=0, vmax=30,  # temperature range
       cmap='viridis',
       cb_lbl='Temperature (°C)'
   )

Create a KML file for Google Earth:

.. code-block:: python

   from remote_sensing import kml

   # Create KML with colorbar
   kml.make_kml(
       lon_min, lat_min, lon_max, lat_max,
       ['figure.png'],
       colorbar='colorbar.png',
       kmzfile='output.kmz'
   )

Common Operations
--------------

Combining Multiple Maps
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Load multiple HEALPix maps
   maps = [
       RS_Healpix.from_dataset_file(f, 'sea_surface_temperature')
       for f in files
   ]

   # Average the maps
   combined_map = RS_Healpix.from_list(maps)

Geographic Subsetting
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Load data for specific region
   healpix_map = RS_Healpix.from_dataset_file(
       'sst_file.nc',
       'sea_surface_temperature',
       lat_slice=slice(18, 23),
       lon_slice=slice(127, 134)
   )

Next Steps
---------

- Check out the :doc:`tutorials/index` for more detailed examples
- See the API reference for complete documentation
- Visit the :doc:`contributing` guide to contribute to the project