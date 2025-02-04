""" Methods for SST data download. """

def quality_control(ds):
    """ Sensor / Product specific quality control. """

    bad = None
    if ds.attrs['sensor'] == 'AMSR2':
        bad = ds.quality_level <= 2

    return bad
