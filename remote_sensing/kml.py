""" Methods for working with KML files. """

import simplekml
import matplotlib.pyplot as plt

def png_to_kml(input_file, output_file, var_name, vmin, vmax, cmap='viridis'):
    kml = simplekml.Kml()

    # Add a color scale legend
    screen = kml.newscreenoverlay(name='Color Scale')
    screen.icon.href = 'temp_colorbar.png'
    screen.overlayxy = simplekml.OverlayXY(x=0, y=0,
                                          xunits=simplekml.Units.fraction,
                                          yunits=simplekml.Units.fraction)
    screen.screenxy = simplekml.ScreenXY(x=0.02, y=0.02,
                                        xunits=simplekml.Units.fraction,
                                        yunits=simplekml.Units.fraction)
    screen.size.x = 0.2
    screen.size.y = 0.05
    screen.size.xunits = simplekml.Units.fraction
    screen.size.yunits = simplekml.Units.fraction
    
    # Create and save the colorbar
    fig, ax = plt.subplots(figsize=(6, 1))
    plt.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(vmin, vmax), cmap=cmap),
                cax=ax, orientation='horizontal',
                label=f'{var_name.upper()} (°C)')
    plt.savefig('temp_colorbar.png', bbox_inches='tight', dpi=100)
    plt.close()
    
    # Save the KML file
    kml.save(output_file)


def scatter_to_kml_advanced(lon, lat, colors=None, sizes=None, labels=None, output_file='output.kml'):
    kml = simplekml.Kml()
    
    for i, (lo, la) in enumerate(zip(lon, lat)):
        pnt = kml.newpoint()
        pnt.coords = [(lo, la)]
        
        # Add style
        if colors is not None:
            pnt.style.iconstyle.color = colors[i]
        if sizes is not None:
            pnt.style.iconstyle.scale = sizes[i]
        if labels is not None:
            pnt.name = str(labels[i])
            
        # Additional styling options
        pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
        
    kml.save(output_file)