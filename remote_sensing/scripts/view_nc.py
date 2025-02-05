""" Script to view a variable in a NetCDF file """

from IPython import embed

def parser(options=None):
    import argparse
    # Parse
    parser = argparse.ArgumentParser(description='View a variable in a NetCDF file')
    parser.add_argument("netcdf_file", type=str, help="File+path to NetCDF file")
    parser.add_argument("variable", type=str, help="Variable to view (or a 'shortcut', e.g. sst)")
    # Optional arguments
    parser.add_argument("--lat_min", type=float, help="Minimum latitude")
    parser.add_argument("--lat_max", type=float, help="Maximum latitude")
    parser.add_argument("--lon_min", type=float, help="Minimum longitude")
    parser.add_argument("--lon_max", type=float, help="Maximum longitude")  
    parser.add_argument("--projection", type=str, default='mollweide', help="Projection for the plot; (mollweide, platecarree)")

    parser.add_argument("--itime", type=int, default=0, help="Time index to view, if applicable")

    if options is None:
        pargs = parser.parse_args()
    else:
        pargs = parser.parse_args(options)
    return pargs


def main(pargs):
    """ Run
    """
    import numpy as np
    from matplotlib import pyplot as plt
    import xarray

    from remote_sensing.plotting import globe


    # Load 
    ds = xarray.open_dataset(pargs.netcdf_file)

    found_it = False
    if pargs.variable in ds.variables:
        found_it = True
        variable = pargs.variable
    elif pargs.variable == 'sst':
        for variable in ['sea_surface_temperature', 'analysed_sst']:
            if variable in ds.variables:
                found_it = True
                break

    if not found_it:
        raise IOError("Variable not found in the NetCDF file")

    da = ds[variable]
    # Time?
    if 'time' in da.dims:
        da = da.isel(time=pargs.itime)

    # Unpack
    if da.lat.ndim == 2:
        lats = da.lat.values
        lons = da.lon.values
    elif da.lat.ndim == 1:
        # Convert to 2D
        lons, lats = np.meshgrid(da.lon.values, da.lat.values)
    else:
        raise ValueError("Bad lat/lon shape")

    # Masked array for the values
    vals = np.ma.array(da.values)

    # Mask me
    bad = np.isnan(vals)
    vals.mask = bad

    # BBOX
    lon_lim = [None, None]
    lat_lim = [None, None]
    if pargs.lat_min is not None:
        lat_lim[0] = pargs.lat_min
    if pargs.lat_max is not None:
        lat_lim[1] = pargs.lat_max
    if pargs.lon_min is not None:
        lon_lim[0] = pargs.lon_min
    if pargs.lon_max is not None:
        lon_lim[1] = pargs.lon_max
        

    # Options
    kwargs = {}
    kwargs['show'] = True
    kwargs['lon_lim'] = lon_lim
    kwargs['lat_lim'] = lat_lim
    kwargs['projection'] = pargs.projection

    # Plot
    ax, im = globe.plot_lons_lats_vals(lons, lats, vals, **kwargs)
