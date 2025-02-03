""" Utility functions for working with HEALPix data. """


import healpy as hp
import numpy as np

import xarray

def get_nside_from_angular_size(angular_size_deg):
    """
    Find the appropriate HEALPix NSIDE parameter for a given angular size in degrees.
    Returns the NSIDE value that gives pixel sizes just smaller than the requested size.
    
    Parameters:
    -----------
    angular_size_deg : float
        Desired angular resolution in degrees
        
    Returns:
    --------
    nside : int
        HEALPix NSIDE parameter (must be a power of 2)
    actual_pixel_size : float
        Actual pixel size in degrees for the returned NSIDE
    """
    
    # Convert degrees to radians
    angular_size_rad = np.deg2rad(angular_size_deg)
    
    # HEALPix pixel area is approximately (4*pi)/(12*NSIDE^2) steradians
    # For small angles, pixel size ≈ sqrt(pixel area)
    # Solve for NSIDE
    nside_exact = np.sqrt(np.pi/(3 * angular_size_rad**2))
    
    # NSIDE must be a power of 2
    # Get the next power of 2 that gives bigger pixels than requested
    nside = 2**(np.ceil(np.log2(nside_exact))-1)
    
    # Calculate actual pixel size for this NSIDE
    pixel_area_rad = hp.nside2pixarea(int(nside))
    actual_pixel_size_deg = np.rad2deg(np.sqrt(pixel_area_rad))
    
    return int(nside), actual_pixel_size_deg

# Example usage:
# angular_size = 1.0  # degrees
# nside, pixel_size = get_nside_from_angular_size(angular_size)
# print(f"For {angular_size}° resolution, use NSIDE={nside} (actual pixel size: {pixel_size:.2f}°)")

def get_nside_from_dataset(ds:xarray.Dataset):
    """
    Find the appropriate HEALPix NSIDE parameter for a given xarray Dataset.
    Returns the NSIDE value that gives pixel sizes just smaller than the smallest pixel size in the dataset.
    
    Parameters:
    -----------
    ds : xarray.Dataset
        Dataset containing HEALPix data
        
    Returns:
    --------
    nside : int
        HEALPix NSIDE parameter (must be a power of 2)
    actual_pixel_size : float
        Actual pixel size in degrees for the returned NSIDE
    """
    
    # Find the median latitude setp size
    delta_lat = np.nanmedian(np.diff(ds.lat))

    # nside
    return get_nside_from_angular_size(delta_lat)