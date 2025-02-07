""" Methods for SST data download. """

def quality_control(ds):
    """ Sensor / Product specific quality control. """

    bad = None
    if ds.attrs['sensor'] == 'AMSR2':
        bad = ds.quality_level < 2
    elif ds.attrs['sensor'] == 'VIIRS':
        bad = ds.quality_level < 5
    elif ds.attrs['sensor'] == 'AHI':
        bad = ds.quality_level < 5

    return bad
