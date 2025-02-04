""" Fuss about with units """


def kelvin_to_celsius(da):
    """Convert temperature DataArray from Kelvin to Celsius."""
    return (da - 273.15).assign_attrs({
        **da.attrs,
        'units': '°C',
        'long_name': da.attrs.get('long_name', 'Temperature') + ' in Celsius'
    })