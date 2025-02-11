HEALPix Module
=============

The HEALPix module provides tools for working with HEALPix (Hierarchical Equal Area isoLatitude Pixelization) maps.

RS_Healpix Class
---------------

.. autoclass:: remote_sensing.rs_healpix.RS_Healpix
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: __init__

Properties
~~~~~~~~~

.. code-block:: python

   @property
   def lons_lats(self):
       """Return the latitudes and longitudes of all pixels."""

   @property
   def lats(self):
       """Return the latitudes of all pixels."""

   @property
   def lons(self):
       """Return the longitudes of all pixels."""

   @property
   def pix_resol(self):
       """Return the pixel resolution in degrees."""

   @property
   def pix_area(self):
       """Return the pixel area in square degrees."""

Class Methods
~~~~~~~~~~~~

.. code-block:: python

   @classmethod
   def from_list(cls, rs_list):
       """Initialize from a list of RS_Healpix objects."""

   @classmethod
   def from_dataset_file(cls, filename, variable, lat_slice=None, lon_slice=None):
       """Initialize from a dataset file."""

   @classmethod
   def from_dataarray(cls, da, nside=None):
       """Initialize from an xarray DataArray."""

Utility Functions
---------------

.. automodule:: remote_sensing.healpix.utils
   :members:
   :undoc-members:
   :show-inheritance:

Key Functions
~~~~~~~~~~~~

.. code-block:: python

   def get_nside_from_angular_size(angular_size_deg):
       """Find appropriate HEALPix NSIDE parameter for given angular size."""

   def get_nside_from_dataset(ds):
       """Find appropriate HEALPix NSIDE parameter for given dataset."""

   def da_to_healpix(da, stat='mean', nside=None):
       """Convert DataArray to HEALPix format."""

   def masked_in_box(hp, box):
       """Find masked HEALPix pixels within bounding box."""

Combining HEALPix Maps
--------------------

.. automodule:: remote_sensing.healpix.combine
   :members:
   :undoc-members:
   :show-inheritance:

.. code-block:: python

   def average_masked_arrays(arrs):
       """Average multiple masked arrays preserving valid values."""