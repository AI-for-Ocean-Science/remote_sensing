""" Test routines for podaac.py """

import pytest

from remote_sensing.download import podaac

#def test_grab_files():
""" Test the grab_files method. """
podaac.grab_file_list('AMSR2-REMSS-L2P_RT-v8.2', verbose=False)
assert True
