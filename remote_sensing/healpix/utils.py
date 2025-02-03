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



def evals_to_healpix(ds:xarray.Dataset,
                     stat:str='mean'):
    """
    Generate a healpix map of where the input
    MHW Systems are located on the globe

    Parameters
    ----------
    ds : xa.Dataset
    stat : str, optional
        Statistic to calculate. Default is 'mean'
    
    Returns
    -------
    healpix_array : hp.ma (number of items contributing)
    healpix_array : hp.ma1 (combined statistic)
    lats : np.ndarray
    lons : np.ndarray
    """
    # Unpack
    if ds.lat.ndim == 2:
        lats = ds.lat.values
        lons = ds.lon.values
    elif ds.lat.ndim == 1:
        # Convert to 2D
        lons, lats = np.meshgrid(ds.lon.values, ds.lat.values)
    else:
        raise ValueError("Bad lat/lon shape")
    
    # Deal with NaNs
    vals = ds.data
    finite = np.isfinite(vals)

    # Healpix coords
    theta = (90 - lats) * np.pi / 180. 
    phi = lons * np.pi / 180.
    nside, _ = get_nside_from_dataset(ds)
    idx_all = hp.pixelfunc.ang2pix(nside, theta, phi)

    # Count events
    npix_hp = hp.nside2npix(nside)
    all_events = np.ma.masked_array(np.zeros(npix_hp, dtype='int'))
    all_values = np.ma.masked_array(np.zeros(npix_hp, dtype='float'))

    # Calculate median values
    pixels = np.unique(idx_all)

    for pixel in pixels:
    
        # find where which cutouts to put in that pixel
        mtch = (pixel == idx_all) & finite
        icount = np.sum(mtch) 

        if icount == 0:
            continue
        all_events[pixel] = icount

        if stat == 'mean':
            all_values[pixel] = np.mean(vals[mtch])
        elif stat == 'median':
            all_values[pixel] = np.median(vals[mtch])
        else:
            raise ValueError(f"Bad stat: {stat}")


    # Mask 

    hpma = hp.ma(all_events.astype(float))
    hpma1 = hp.ma(all_values)

    zero = all_events == 0 
    hpma.mask = zero # current mask set to zero array, where Trues (no events) are masked
    hpma1.mask = zero 

    # Angles (convenient)
    hp_lons, hp_lats = hp.pixelfunc.pix2ang(nside, np.arange(npix_hp), lonlat=True)

    # Return
    return hpma, hpma1, hp_lons, hp_lats, nside