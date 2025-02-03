""" A light-weight class for holding HEALPix maps 
for Remote Sensing. """

from importlib import reload

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

    @property
    def pix_resol(self):
        """ Return the pixel size in degrees. """
        return hp.nside2resol(self.nside, arcmin=True) / 60.

    @property
    def pix_area(self):
        """ Return the pixel area in square degrees. """
        return hp.nside2pixarea(self.nside, degrees=True)

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