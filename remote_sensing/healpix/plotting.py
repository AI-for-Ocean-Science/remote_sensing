""" Routines to plot healpix data. """

import numpy as np

from matplotlib import pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


def plot_rs_hp(rs_hp, tricontour=False, 
               cb_lbl=None, figsize=(12,8), 
               vmin:float=None, vmax:float=None,
               projection:str=None,
               ssize:float=1.,
               cb_lsize:float=15.,
               cb_tsize:float=13.,
               color='viridis', show=False,
               ax=None):
    """Generate a global map of mean LL of the input
    cutouts
    Args:
        rs_hp (RS_Healpix): RS_Healpix object
        tricontour (bool, optional): [description]. Defaults to False.
        lbl ([type], optional): [description]. Defaults to None.
        figsize (tuple, optional): [description]. Defaults to (12,8).
        color (str, optional): [description]. Defaults to 'Reds'.
        vmin (float, optional): [description]. Defaults to None.
        vmax (float, optional): [description]. Defaults to None.
        show (bool, optional): If True, show on the screen.  Defaults to True
    Returns:
        matplotlib.Axis: axis holding the plot
    """
    # Unpack
    hp_values = rs_hp.hp
    hp_lons = rs_hp.lons
    hp_lats = rs_hp.lats
    
    # Figure
    if ax is None:
        fig = plt.figure(figsize=figsize)
        plt.clf()

    tformM = ccrs.Mollweide()
    tformP = ccrs.PlateCarree()

    if projection is None:
        tform = None
    elif projection == 'mollweide':
        tform = tformM
    elif projection == 'platecarree':
        tform = tformP
    else:
        raise ValueError(f"Bad projection: {projection}")

    if ax is None:
        ax = plt.axes(projection=tform)

    if tricontour:
        cm = plt.get_cmap(color)
        img = ax.tricontourf(hp_lons, hp_lats, hp_values, 
                             transform=tform,
                         levels=20, cmap=cm)#, zorder=10)
    else:
        cm = plt.get_cmap(color)
        # Cut
        good = np.invert(hp_values.mask)
        img = ax.scatter(x=hp_lons[good],
            y=hp_lats[good],
            c=hp_values[good], 
            vmin=vmin, vmax=vmax,
            cmap=cm,
            s=ssize,
            transform=tformP)

    # Colorbar
    cb = plt.colorbar(img, orientation='horizontal', pad=0.)
    if cb_lbl is not None:
        cb.set_label(cb_lbl, fontsize=cb_lsize)
    cb.ax.tick_params(labelsize=cb_tsize)

    # Coast lines
    if not tricontour:
        ax.coastlines(zorder=10)
        ax.set_global()
    
        gl = ax.gridlines(crs=ccrs.PlateCarree(), linewidth=1, 
            color='black', alpha=0.5, linestyle=':', draw_labels=True)
        gl.xlabels_top = False
        gl.ylabels_left = True
        gl.ylabels_right=False
        gl.xlines = True
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        gl.xlabel_style = {'color': 'black'}# 'weight': 'bold'}
        gl.ylabel_style = {'color': 'black'}# 'weight': 'bold'}
        #gl.xlocator = mticker.FixedLocator([-180., -160, -140, -120, -60, -20.])
        #gl.xlocator = mticker.FixedLocator([-240., -180., -120, -65, -60, -55, 0, 60, 120.])
        #gl.ylocator = mticker.FixedLocator([0., 15., 30., 45, 60.])


    # Layout and save
    if show:
        plt.show()

    return ax
