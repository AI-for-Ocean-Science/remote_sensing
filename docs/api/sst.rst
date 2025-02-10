Sea Surface Temperature (SST) Module
================================

The SST module provides functionality for handling and processing sea surface temperature data from various sensors.

Main Functions
-------------

.. automodule:: remote_sensing.sst
   :members:
   :undoc-members:
   :show-inheritance:

Data Loading
~~~~~~~~~~~

.. code-block:: python

   def load(filename, verbose=True):
       """
       Load SST data from a NetCDF file.

       Parameters
       ----------
       filename : str
           NetCDF file to load (must include time dimension)
       verbose : bool, optional
           Whether to print status messages

       Returns
       -------
       tuple
           (sst, qual, latitude, longitude, time)
           Returns None values if data is corrupt
       """

Variable Detection
~~~~~~~~~~~~~~~~

.. code-block:: python

   def find_variable(ds, verbose=False):
       """
       Find the SST variable in a dataset.

       Parameters
       ----------
       ds : xarray.Dataset
           Dataset to search
       verbose : bool, optional
           Whether to print found variable

       Returns
       -------
       str or None
           Variable name if found
       """

Quality Control
~~~~~~~~~~~~~

.. code-block:: python

   def quality_control(ds):
       """
       Apply sensor-specific quality control.

       Parameters
       ----------
       ds : xarray.Dataset
           Dataset with quality information

       Returns
       -------
       numpy.ndarray or None
           Mask of bad values
       """

Supported Sensors
---------------

The module supports quality control for the following sensors:

* AMSR2 (quality_level >= 2)
* VIIRS (quality_level >= 5)
* AHI (quality_level >= 5)

Unit Conversion
-------------

.. automodule:: remote_sensing.units
   :members:
   :undoc-members:
   :show-inheritance:

.. code-block:: python

   def kelvin_to_celsius(da):
       """
       Convert temperature DataArray from Kelvin to Celsius.
       
       Updates attributes to reflect the new units.
       """