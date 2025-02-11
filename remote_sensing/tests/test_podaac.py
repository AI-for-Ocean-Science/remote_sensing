""" Test routines for podaac.py """

import pytest

from remote_sensing.download import podaac

def test_grab_file_list():
    """ Test the grab_files method. """
    podaac.grab_file_list('AMSR2-REMSS-L2P_RT-v8.2', verbose=False)
    assert True

def test_grab_file_list_with_bbox():
    """ Test the grab_files method. """
    podaac.grab_file_list('AMSR2-REMSS-L2P_RT-v8.2', 
        bbox="127,18,134,23", verbose=False)

def test_download():
    # Test the download_files method
    file_list = ['https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-protected/AMSR2-REMSS-L2P_RT-v8.2/20250126201242-REMSS-L2P_GHRSST-SSTsubskin-AMSR2-L2B_rt_r67530-v02.0-fv01.0.nc', 
             'https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-protected/AMSR2-REMSS-L2P_RT-v8.2/20250126183349-REMSS-L2P_GHRSST-SSTsubskin-AMSR2-L2B_rt_r67529-v02.0-fv01.0.nc']

    podaac.download_files(file_list, verbose=False)

