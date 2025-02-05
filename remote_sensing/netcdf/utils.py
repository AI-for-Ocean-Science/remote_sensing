""" Utilities for working with netCDF files. """

import xarray

from . import sst

def gen_mask_for_dataset(ds:xarray.Dataset, variable:str):
    """
    Generate a mask for a dataset based on a variable.

    Parameters
    ----------
    ds : xarray.Dataset
        Dataset containing the variable
    variable : str
        Variable name

    Returns
    -------
    mask : numpy.ndarray
        Mask for the variable
    """
    mask = None

    # Quality control
    if variable in ['sea_surface_temperature', 'analysed_sst']:
        mask = sst.quality_control(ds)
    
    return mask