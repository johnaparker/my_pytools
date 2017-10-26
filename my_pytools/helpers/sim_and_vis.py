import argparse
import h5py
import os
import sys

class Bunch:
    """Simply convert a dictionary into a class with data members equal to the dictionary keys"""
    def __init__(self, adict):
        self.__dict__.update(adict)

def load_symbols(filepath):
    """Load all symbols from h5 filepath"""
    symbols = {}
    with h5py.File(filepath, 'r') as f:
        for dset in f:
            symbols[dset] = f[dset][...]
    return Bunch(symbols)

def write_symbols(filepath, symbols):
    """Write all symbols to h5 file, where symbols is a {name: value} dictionary"""
    with h5py.File(filepath, 'w') as f:
        for name,symbol in symbols.items():
            f[name] = symbol

class sim_and_vis:
    """Control over simulation and visualization functions"""
    def __init__(self, filepath):
        """filepath to hdf5 file"""
        self.filepath = filepath

        parser = argparse.ArgumentParser()
        parser.add_argument('action', nargs='?', type=str, choices=['sim', 'vis', 'both'], default='vis', help='Run the sim, vis the results, or do both')
        self.args = parser.parse_args()

    def request(self):
        """request if existing hdf5 file should be overwriten"""
        if os.path.exists(self.filepath):
            delete = input(f"Do you really want to write over existing data in '{self.filepath}'? (y/n) ")
            if delete != 'y':
                sys.exit('Aborting...')

    def write(self, symbols):
        """write symbols"""
        write_symbols(self.filepath, symbols)

    def read(self):
        """read symbols"""
        return load_symbols(self.filepath)

    def execute(self, sim, vis):
        """given sim() and vis() functions, run the request"""
        if self.args.action in ['sim', 'both']:
            self.request()
            print("Running simulation...")
            symbols = sim()
            self.write(symbols)

        if self.args.action in ['vis', 'both']:
            print("Visualizing data...")
            vis()

if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    # Setup
    print("Script is running")
    filepath = 'data.h5'
    job = sim_and_vis(filepath)

    # Fast, shared code goes here
    x = np.linspace(0,1,100)

    def sim():
        # Slow, sim-only code goes here and relevant data is written to file
        y = x**2
        return {'y': y}

    def vis():
        # Process/Visualize data here after loading symbols from file
        symbols = job.read()

        plt.plot(x, symbols.y)
        plt.show()

    # execute
    job.execute(sim,vis)
