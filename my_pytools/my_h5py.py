import h5py

def write_over(group, name, data):
    """write over group[data] if it exists, otherwise create it
               group           group or file object
               name            name of dataset
               data            data to write
    """
    if name in group:
        group[name][...] = data
    else:
        group[name] = data
