""" Methods to combine multiple healpix images into a single image. """


import numpy as np
import numpy.ma as ma

def average_masked_arrays(arrs:list):
    """
    Average a list of masked arrays, using values that exist in either array.
    If a value exists in only one array, use that value instead of masking it.
    
    Parameters:
    -----------
    list : numpy.ma.MaskedArray
        Input masked arrays to average
        
    Returns:
    --------
    numpy.ma.MaskedArray
        Averaged array, preserving values that exist in at least one input
    """
    # Count valid (non-masked) values at each position
    valid_count = np.zeros(arrs[0].size)
    summed = valid_count.copy()
    for arr in arrs:
        valid_count += (1-arr.mask.astype(int))
        # Sum the arrays, treating masked values as 0
        summed += arr.filled(0)
    
    # Create mask for positions where both values are masked/NaN
    final_mask = valid_count == 0
    
    # Divide by count of valid values (1 or 2) to get average
    # Note: divide by 1 where only one value exists
    result = ma.array(summed / np.maximum(valid_count, 1), mask=final_mask)
    
    return result