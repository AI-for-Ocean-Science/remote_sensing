SST Data Analysis Tutorial
=====================

This tutorial demonstrates how to work with Sea Surface Temperature (SST) data using the Remote Sensing package.

Loading and Quality Control
------------------------

First, let's load some SST data and apply quality control:

.. code-block:: python

   from remote_sensing import sst
   from remote_sensing.netcdf import utils as nc_utils

   # Load SST data
   filename = 'AMSR2_sst_20250201.nc'
   sst_data, quality, lat, lon, time = sst.load(filename)

   # Check data properties
   print(f"Time: {time}")
   print(f"Latitude range: {lat.min():.2f} to {lat.max():.2f}")
   print(f"Longitude range: {lon.min():.2f} to {lon.max():.2f}")
   print(f"Temperature range: {sst_data.min():.1f}°C to {sst_data.max():.1f}°C")

   # Apply quality control
   mask = nc_utils.build_mask(
       sst_data, 
       quality,
       qual_thresh=5,  # Minimum quality level
       temp_bounds=(-2, 33)  # Valid temperature range
   )

   # Mask invalid data
   sst_data[mask] = np.nan

Converting to HEALPix
------------------

Now let's convert our SST data to HEALPix format for efficient global analysis:

.. code-block:: python

   from remote_sensing.rs_healpix import RS_Healpix
   import xarray as xr

   # Create DataArray
   da = xr.DataArray(
       sst_data,
       coords={'lat': lat, 'lon': lon},
       dims=['lat', 'lon'],
       attrs={'units': '°C'}
   )

   # Convert to HEALPix
   hp_map = RS_Healpix.from_dataarray(da)

   print(f"HEALPix resolution: {hp_map.pix_resol:.2f} degrees")
   print(f"Number of pixels: {hp_map.npix}")

Regional Analysis
--------------

Let's analyze SST patterns in a specific region:

.. code-block:: python

   # Define region of interest
   bbox = (127, 134, 18, 23)  # Western Pacific region

   # Find pixels in region
   from remote_sensing.healpix import utils as hp_utils
   region_pixels = hp_utils.masked_in_box(hp_map.hp, bbox)

   # Get regional statistics
   regional_temps = hp_map.hp.data[~hp_map.hp.mask]
   print(f"Mean temperature: {regional_temps.mean():.1f}°C")
   print(f"Standard deviation: {regional_temps.std():.1f}°C")

Time Series Analysis
-----------------

Now let's analyze SST changes over time:

.. code-block:: python

   import glob
   
   # Get list of SST files
   sst_files = glob.glob('AMSR2_sst_*.nc')
   sst_files.sort()

   # Create HEALPix maps for each file
   maps = []
   for f in sst_files:
       hp = RS_Healpix.from_dataset_file(
           f,
           'sea_surface_temperature',
           lat_slice=slice(18, 23),
           lon_slice=slice(127, 134)
       )
       maps.append(hp)

   # Combine maps
   mean_map = RS_Healpix.from_list(maps)

Visualization
-----------

Finally, let's visualize our results:

.. code-block:: python

   # Create global map
   mean_map.plot(
       vmin=0, 
       vmax=30,
       cmap='viridis',
       cb_lbl='Mean SST (°C)',
       projection='platecarree',
       lon_lim=(120, 140),
       lat_lim=(15, 25)
   )

   # Save as KML for Google Earth
   from remote_sensing import kml

   kml.make_kml(
       120, 15, 140, 25,  # bounds
       ['sst_map.png'],
       colorbar='colorbar.png',
       kmzfile='sst_analysis.kmz'
   )

This tutorial covered the basics of working with SST data. For more advanced topics, check out the other tutorials in this series.