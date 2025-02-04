""" Routines to plot healpix data. """

import numpy as np

from matplotlib import pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


def plot_rs_hp(rs_hp, tricontour=False, 
               figsize=(12,8), 
               vmin:float=None, vmax:float=None,
               projection:str='mollweide',
               ssize:float=1.,
               add_colorbar:bool=True,
               cb_lbl=None, 
               cb_lsize:float=14.,
               cb_tsize:float=12.,
               dpi:int=300,
               marker:str=None,
               cmap='viridis', show=False,
               xlim:tuple=None, ylim:tuple=None,
               ax=None, savefig:str=None,
               transparent:bool=True):
    """Generate a global map of mean LL of the input
    cutouts
    Args:
        rs_hp (RS_Healpix): RS_Healpix object
        tricontour (bool, optional): Use tricontour.  Defaults to False.
        figsize (tuple, optional): Size of the figure.  Defaults to (12,8).
        vmin (float, optional): Minimum value for the color scale.  Defaults to None.
        vmax (float, optional): Maximum value for the color scale.  Defaults to None.
        projection (str, optional): Projection for the plot.  Defaults to 'mollweide'.
        ssize (float, optional): Size of the points.  Defaults to 1..
        add_colorbar (bool, optional): Add a colorbar.  Defaults to True.
        cb_lbl ([type], optional): Label for the colorbar.  Defaults to None.
        cb_lsize (float, optional): Label size for the colorbar.  Defaults to 14..
        cb_tsize (float, optional): Tick size for the colorbar.  Defaults to 12..
        cmap (str, optional): Colormap.  Defaults to 'viridis'.
        show (bool, optional): Show the plot.  Defaults to False.
        xlim (tuple, optional): x limits.  Defaults to None.
        ylim (tuple, optional): y limits.  Defaults to None.
        ax ([type], optional): Axis to use.  Defaults to None.
        savefig (str, optional): If not None, save the figure to this file.  Defaults to None
        transparent (bool, optional): Make the background transparent.  Defaults to True.
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

    if projection == 'mollweide':
        tform = tformM
    elif projection == 'platecarree':
        tform = tformP
    else:
        raise ValueError(f"Bad projection: {projection}")

    if ax is None:
        ax = plt.axes(projection=tform)

    if tricontour:
        cm = plt.get_cmap(cmap)
        img = ax.tricontourf(hp_lons, hp_lats, hp_values, 
                             transform=tform,
                         levels=20, cmap=cm)#, zorder=10)
    else:
        cm = plt.get_cmap(cmap)
        # Cut
        good = np.invert(hp_values.mask)
        img = ax.scatter(x=hp_lons[good],
            y=hp_lats[good],
            c=hp_values[good], 
            vmin=vmin, vmax=vmax,
            marker=marker,
            cmap=cm,
            s=ssize,
            transform=tformP)

    # Colorbar
    if add_colorbar:
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

    # Limits
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)

    plt.tight_layout()

    # Save?
    if savefig is not None:
        plt.savefig(savefig, bbox_inches='tight', dpi=dpi,
                    transparent=transparent)

    # Layout and save
    if show:
        plt.show()

    return ax, img
