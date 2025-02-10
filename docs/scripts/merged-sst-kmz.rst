Merged SST to KMZ Script
========================

A Python script that merges microwave (AMSR2) and infrared (Himawari-9) sea surface temperature (SST) products and generates a KMZ file for visualization in Google Earth.

Overview
--------

This script was developed for the ARCTERX 2025, Leg 2 campaign to combine the strengths of two different SST products:

- AMSR2: Microwave-based measurements that can see through clouds
- Himawari-9 AHI: High-resolution infrared measurements with better spatial resolution

The script downloads recent data from both sources, combines them using HEALPix mapping, and creates a KMZ file for easy visualization in Google Earth.

Usage
-----

.. code-block:: bash

    python merged_sst_to_kmz.py [options]

Options
~~~~~~~

Required Authentication
    - Must have Earthdata credentials configured for PODAAC access

Optional Arguments
    --namsr2 INT
        Number of AMSR2 exposures to combine (default: 1)
    
    --nh09 INT
        Number of hours of Himawari images to combine (default: 10)
    
    --ndays INT
        Number of days into the past to consider for images (default: 2)
    
    --t_end STR
        End time in ISO format (e.g., "2025-02-07T04:00:00Z")
    
    --debug
        Enable debug mode
    
    -s, --show
        Show extra plots during processing
    
    --verbose
        Print more information to screen
    
    --clobber
        Overwrite existing files
    
    --use_json STR
        Load files from a previously generated JSON file

Operation
--------

The script performs the following steps:

1. Data Acquisition
    - Downloads recent AMSR2 and Himawari-9 data from PODAAC
    - Files are saved locally and paths are recorded in a JSON file

2. HEALPix Processing
    - Converts both SST products to HEALPix format
    - AMSR2 data is processed at ~11km resolution
    - Multiple images can be stacked and averaged

3. Data Merging
    - Creates a base map from the higher resolution Himawari-9 data
    - Fills gaps using the AMSR2 data
    - Focuses on the region: 127°-134°E, 18°-23°N

4. KMZ Generation
    - Creates a high-resolution image of the merged SST field
    - Adds a color scale
    - Packages everything into a KMZ file for Google Earth

Output Files
-----------

- ``Merged_SST_YYYYMMDD_HH.json``
    JSON file containing the paths to downloaded data files

- ``Merged_SST_YYYYMMDD_HH.kmz``
    Final KMZ file for Google Earth visualization

Dependencies
-----------

- xarray: For NetCDF file handling
- numpy: For numerical operations
- matplotlib: For plotting
- cartopy: For map projections
- healpy: For HEALPix operations
- simplekml: For KMZ file creation

This script is part of the Remote Sensing package and relies on several of its modules:

- remote_sensing.download.podaac
- remote_sensing.healpix.rs_healpix
- remote_sensing.io
- remote_sensing.kml

Example
-------

.. code-block:: bash

    # Generate a merged SST product for the last 24 hours
    python merged_sst_to_kmz.py --namsr2 2 --nh09 12 --ndays 1 --show

    # Use a specific end time
    python merged_sst_to_kmz.py --t_end "2025-02-07T04:00:00Z" --verbose

    # Reprocess using previously downloaded files
    python merged_sst_to_kmz.py --use_json Merged_SST_20250207_04.json
