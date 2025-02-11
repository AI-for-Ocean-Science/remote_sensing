Visualization Module
===================

Tools for visualizing remote sensing data, including global maps and KML file generation.

Globe Plotting
-------------

.. automodule:: remote_sensing.plotting.globe
   :members:
   :undoc-members:
   :show-inheritance:

Main Plotting Function
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def plot_lons_lats_vals(lons, lats, values, **kwargs):
       """
       Generate a global map visualization.

       Parameters
       ----------
       lons : numpy.ndarray
           Longitudes
       lats : numpy.ndarray
           Latitudes
       values : numpy.ndarray
           Values to plot
       **kwargs : dict
           Additional plotting parameters

       Key Parameters
       -------------
       tricontour : bool
           Use tricontour instead of scatter (default: False)
       projection : str
           Map projection ('mollweide' or 'platecarree')
       vmin, vmax : float
           Color scale limits
       cmap : str
           Colormap name
       add_colorbar : bool
           Whether to add a colorbar
       savefig : str
           If provided, save figure to this path

       Returns
       -------
       tuple
           (matplotlib.Axis, matplotlib.image)
       """

KML Generation
-------------

.. automodule:: remote_sensing.kml
   :members:
   :undoc-members:
   :show-inheritance:

Key Functions
~~~~~~~~~~~

.. code-block:: python

   def make_kml(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat,
                figs, colorbar=None, **kw):
       """
       Create KML file from matplotlib figures.

       Parameters
       ----------
       llcrnrlon, llcrnrlat : float
           Lower left corner coordinates
       urcrnrlon, urcrnrlat : float
           Upper right corner coordinates
       figs : list
           List of figure filenames
       colorbar : str, optional
           Colorbar figure filename
       **kw : dict
           Additional KML parameters
       """

   def colorbar(im, label, filename):
       """
       Create colorbar figure for KML overlay.

       Parameters
       ----------
       im : matplotlib.image.AxesImage
           Image for colorbar
       label : str
           Colorbar label
       filename : str
           Output filename
       """

   def scatter_to_kml_advanced(lon, lat, colors=None, sizes=None, 
                             labels=None, output_file='output.kml'):
       """
       Create KML file from scatter plot data with advanced styling.

       Parameters
       ----------
       lon, lat : array-like
           Coordinates
       colors : array-like, optional
           Point colors
       sizes : array-like, optional
           Point sizes
       labels : array-like, optional
           Point labels
       output_file : str
           Output KML filename
       """