""" A light-weight class for holding HEALPix maps 
for Remote Sensing. """

from importlib import reload
import os

import numpy as np
import healpy as hp
import xarray

from remote_sensing.healpix import utils as hp_utils 
from remote_sensing.healpix import plotting as hp_plotting
from remote_sensing.healpix import combine as hp_combine
from remote_sensing import units

from IPython import embed

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

    @property
    def basename(self):
        """ Return the pixel area in square degrees. """
        if self.filename is not None:
            return os.path.basename(self.filename)

    @classmethod
    def from_list(cls, rs_list:list):
        """
        Initialize the RS_Healpix object from a list of RS_Healpix objects.

        Parameters
        ----------
        rs_list : list
            List of RS_Healpix objects to average

        Returns
        -------
        RS_Healpix

        """
        # Check
        nside = rs_list[0].nside
        for rs in rs_list:
            if rs.nside != nside:
                raise ValueError("All RS_Healpix objects must have the same NSIDE")
                
        # Average
        hp_values = hp_combine.average_masked_arrays([rs.hp for rs in rs_list])
        hp_lons = rs_list[0].lons
        hp_lats = rs_list[0].lats

        # Instantiate
        rsh = RS_Healpix(nside)
        rsh.hp = hp_values
        rsh.lons = hp_lons
        rsh.lats = hp_lats

        # A bit more
        if rs_list[0].filename is not None:
            rsh.filename = f'Avg[{rs_list[0].basename}-{rs_list[-1].basename}]'
        if rs_list[0].variable is not None:
            rsh.variable = rs_list[0].variable

        # Return
        return rsh

    @classmethod
    def from_dataset_file(cls, filename:str, variable:str, 
                            lat_slice:slice=None, 
                            lon_slice:slice=None,
                            time_isel:int=None,
                            resol_km:float=None):
        """
        Initialize the RS_Healpix object from a dataarray file.

        Parameters
        ----------
        filename : str
            Filename of the dataset file
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
        nside = None
        ds = xarray.open_dataset(filename)
        if ds.lat.ndim == 1:
            if lat_slice is not None:
                ds = ds.sel(lat=lat_slice)
            if lon_slice is not None:
                ds = ds.sel(lon=lon_slice)
        if ds.lat.ndim == 2:
            # Deal with junk
            junk = ds.lat < -1000.
            ds.lat.data[junk] = np.nan
            #
            junk = ds.lon < -1000.
            ds.lon.data[junk] = np.nan

            # Cut with NaNs
            if lat_slice is not None:
                junk = (ds.lat < lat_slice[0]) | (ds.lat > lat_slice[1])
                ds.lat.data[junk] = np.nan
            if lon_slice is not None:
                junk = (ds.lon < lon_slice[0]) | (ds.lon > lon_slice[1])
                ds.lon.data[junk] = np.nan
            # nside 
            if resol_km is None:
                raise ValueError("Must provide resol_km for 2D lat/lon arrays")
            # Translate to deg
            delta_lat = resol_km / 111.1
            nside, _ = hp_utils.get_nside_from_angular_size(delta_lat)
        
        # Time slice
        if time_isel is not None:
            ds = ds.isel(time=time_isel)

        # Instantiate
        # If SST, convert to Celsius
        da = ds[variable]
        if da.units == 'K':
            da = units.kelvin_to_celsius(da)
        rsh =  cls.from_dataarray(da, nside=nside)

        # Fill in
        rsh.filename = filename
        rsh.variable = variable

        # Return
        return rsh

        
    @classmethod
    def from_dataarray(cls, da:xarray.DataArray,
                       nside:int=None):
        """
        Initialize the RS_Healpix object from an xarray dataset.

        Parameters
        ----------
        da : xarray.DataArray
            Dataset containing the HEALPix data
        nside : int, optional

        Returns
        -------
        RS_Healpix

        """
        reload(hp_utils)

        
        hp_counts, hp_values, hp_lons, hp_lats, nside = \
            hp_utils.da_to_healpix(da, nside=nside)

        # Instantiate
        rsh = cls(nside)

        # Fill
        rsh.hp = hp_values
        rsh.lons = hp_lons
        rsh.lats = hp_lats
        rsh.counts = hp_counts

        # Return
        return rsh

    def plot(self, **kwargs):
        """ Plot the HEALPix map. """
        reload(hp_plotting)
        hp_plotting.plot_rs_hp(self, **kwargs)
        

    def __repr__(self):
        rstr = f'<RS_Healpix: nside={self.nside}, resol={self.pix_resol}deg'
        if self.filename is not None:
            rstr = f'{rstr}\n file={self.basename}'
        if self.variable is not None:
            rstr = f'{rstr}, var="{self.variable}"'
        rstr = f'{rstr}>'
        # Return
        return rstr