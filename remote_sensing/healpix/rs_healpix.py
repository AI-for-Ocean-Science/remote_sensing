""" A light-weight class for holding HEALPix maps 
for Remote Sensing. """

from importlib import reload
import os

import numpy as np
import healpy as hp
import xarray

from remote_sensing.healpix import utils as hp_utils 

class RS_Healpix(object):

    def __init__(self, nside:int):
        """
        Initialize the RS_Healpix object.
        Parameters
        ----------
        nside : int
            HEALPix NSIDE parameter (must be a power of 2)
        """
        self.nside = nside
        self.npix = hp.nside2npix(nside)

        self.hp = None
        self.lons = None
        self.lats = None
        self.counts = None

        # File?
        self.filename = None
        self.variable = None

    @property
    def pix_resol(self):
        """ Return the pixel size in degrees. """
        return hp.nside2resol(self.nside, arcmin=True) / 60.

    @property
    def pix_area(self):
        """ Return the pixel area in square degrees. """
        return hp.nside2pixarea(self.nside, degrees=True)

    @classmethod
    def from_dataarray_file(cls, filename:str, variable:str, 
                            lat_slice:slice=None, 
                            lon_slice:slice=None,
                            time_isel:int=None):
        """
        Initialize the RS_Healpix object from a dataarray file.

        Parameters
        ----------
        filename : str
            Filename of the dataarray file
        variable : str
            Variable to extract from the dataarray
        lat_slice : slice, optional
            Slice to apply to the latitude dimension
        lon_slice : slice, optional
            Slice to apply to the longitude dimension

        Returns
        -------
        RS_Healpix

        """
        ds = xarray.open_dataset(filename)
        if lat_slice is not None:
            ds = ds.sel(lat=lat_slice)
        if lon_slice is not None:
            ds = ds.sel(lon=lon_slice)
        # Time slice
        if time_isel is not None:
            ds = ds.isel(time=time_isel)

        # Instantiate
        rsh =  cls.from_dataset(ds[variable])

        # Fill in
        rsh.filename = filename
        rsh.variable = variable

        # Return
        return rsh

        
    @classmethod
    def from_dataset(cls, ds:xarray.Dataset):
        """
        Initialize the RS_Healpix object from an xarray dataset.

        Parameters
        ----------
        ds : xarray.Dataset
            Dataset containing the HEALPix data

        Returns
        -------
        RS_Healpix

        """
        reload(hp_utils)
        hp_counts, hp_values, hp_lons, hp_lats, nside = \
            hp_utils.evals_to_healpix(ds)

        # Instantiate
        rsh = cls(nside)

        # Fill
        rsh.hp = hp_values
        rsh.lons = hp_lons
        rsh.lats = hp_lats
        rsh.counts = hp_counts

        # Return
        return rsh

    def __repr__(self):
        rstr = f'<RS_Healpix: nside={self.nside}, npix={self.npix}'
        if self.filename is not None:
            rstr = f'{rstr}\n file={os.path.basename(self.filename)}'
        if self.variable is not None:
            rstr = f'{rstr}, var="{self.variable}"'
        rstr = f'{rstr}>'
        # Return
        return rstr