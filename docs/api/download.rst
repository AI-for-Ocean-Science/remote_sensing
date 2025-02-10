Download Module
===============

Tools for downloading remote sensing data from PODAAC (Physical Oceanography Distributed Active Archive Center).

PODAAC Interface
--------------

.. automodule:: remote_sensing.download.podaac
   :members:
   :undoc-members:
   :show-inheritance:

Key Functions
~~~~~~~~~~~

.. code-block:: python

   def grab_file_list(collection, dt_past=None, time_range=None, bbox=None):
       """
       Get list of available files from PODAAC.

       Parameters
       ----------
       collection : str
           PODAAC collection identifier
       dt_past : dict, optional
           Time delta for past data (e.g., {'days': 1})
       time_range : tuple, optional
           (start_time, end_time) in ISO format
       bbox : str, optional
           Bounding box 'min_lon,min_lat,max_lon,max_lat'

       Returns
       -------
       tuple
           (data_files, checksums)
       """

   def download_files(data_files, checksums=None, output_dir=None, 
                     clobber=False):
       """
       Download files from PODAAC.

       Parameters
       ----------
       data_files : list
           List of file URLs to download
       checksums : list, optional
           List of file checksums
       output_dir : str, optional
           Download directory (default: $OS_RS/PODAAC/collection)
       clobber : bool, optional
           Whether to overwrite existing files
       """

Authentication
-------------

Authentication is required for downloading from PODAAC. You need to:

1. Have an Earthdata account
2. Setup authentication as described in the `data-subscriber documentation <https://github.com/podaac/data-subscriber>`_

Example Usage
-----------

.. code-block:: python

   from remote_sensing.download import podaac

   # Get recent AMSR2 data
   files, checksums = podaac.grab_file_list(
       'AMSR2-REMSS-L2P_RT-v8.2',
       dt_past={'days': 1},
       bbox='127,18,134,23'
   )

   # Download the files
   podaac.download_files(files)

Directory Structure
-----------------

Downloaded files are organized as follows:

.. code-block:: text

   $OS_RS/
   └── PODAAC/
       └── {collection}/
           └── downloaded_files...

If the ``OS_RS`` environment variable is not set, files are downloaded to ``./PODAAC/{collection}/``.