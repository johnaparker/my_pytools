import numpy as np
from scipy.interpolate import RegularGridInterpolator

def ndinterp(data, *args, method="linear"):
    """given N-dimensional data, and args = x,y,z,..., return function f(args) that
       iterpolates the data with method ('linear' or 'nearest')"""
    fit = RegularGridInterpolator(args, data, method=method)
    return lambda *args: fit(args)
