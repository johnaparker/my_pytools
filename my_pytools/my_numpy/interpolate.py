import numpy as np
from scipy.interpolate import RegularGridInterpolator
from scipy.interpolate import interp1d

def ndinterp(data, *args, method="linear", fill_value = np.nan):
    """given N-dimensional data, and args = x,y,z,..., return function f(args) that
       iterpolates the data with method ('linear' or 'nearest')"""
    fit = RegularGridInterpolator(args, data, method=method, fill_value=fill_value, bounds_error=False)
    return lambda *args: fit(args)

def remap_interpolate(data, variables, new_resolutions, method="linear", fill_value = np.nan):
    """ Interpolate an existing dataset to a different resolution
                data                  N-d data
                variables[N]          list of 1-d variables     
                new_resolutions[N]    list of new resolutions for each variable (optionally, a single number for all variables) 
                method                method of interpolation
                fill_value            fill value for values outside domain      """

    num_variables = len(variables)
    if not hasattr(new_resolutions, '__iter__'):
        new_resolutions = np.ones(num_variables)*new_resolutions

    fitted_function = ndinterp(data, *variables, method=method, fill_value=fill_value)

    new_variables = []
    for variable, new_resolution in zip(variables, new_resolutions):
        x = np.arange(0, len(variable))
        f = interp1d(x,variable, kind="linear")
        x_new = np.linspace(0, len(variable)-1, new_resolution)

        new_variables.append( f(x_new) )
    
    new_mesh_variables = np.meshgrid(*new_variables, indexing='ij')
    new_data = fitted_function(*new_mesh_variables)

    return new_mesh_variables, new_data
