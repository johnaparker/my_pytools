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
    sims = {}
    with h5py.File(filepath, 'r') as f:
        for group_name in f:
            group = f[group_name]

            symbols = {}
            for dset_name in group:
                symbols[dset_name] = group[dset_name][...]

            sims[group_name] = Bunch(symbols)

    return Bunch(sims)

def write_symbols(filepath, symbols, group=None):
    """Write all symbols to h5 file, where symbols is a {name: value} dictionary
       
       Arguments:
           filepath      path to file
           symbols       {name: vale} dictionary
           group         group to write symbols to (default: root)
    """
    if group is None:
        group = ''

    with h5py.File(filepath, 'a') as f:
        for name,symbol in symbols.items():
            f[f'{group}/{name}'] = symbol

class sim_and_vis:
    """Control over simulation and visualization functions"""

    def __init__(self, filepath):
        """filepath to hdf5 file"""
        self.filepath = filepath

        parser = argparse.ArgumentParser()
        parser.add_argument('action', nargs='?', type=str, choices=['sim', 'vis', 'both'], default='vis', help='Run the sim, vis the results, or do both')
        parser.add_argument('-f', '--force', action='store_true', help='force over-write any existing files')
        parser.add_argument('-s', '--sims', nargs='*', type=str, default=None, help='run specific sims by name')
        self.args = parser.parse_args()

    def request(self, group=None):
        """request if existing hdf5 file should be overwriten"""
        if group is None:
            group = ''
        
        with h5py.File(self.filepath, 'a') as f:
            if not self.args.force and os.path.exists(self.filepath) and group in f:
                delete = input(f"Do you really want to write over existing data in '{self.filepath}/{group}'? (y/n) ")
                if delete != 'y':
                    sys.exit('Aborting...')
            if group in f:
                del f[group]

    def write(self, symbols, group=None):
        """write symbols"""
        write_symbols(self.filepath, symbols, group)

    def read(self):
        """read symbols"""
        return load_symbols(self.filepath)

    def execute(self, sims, vis, store=None):
        """given {name: sim()} dictionary and {name: vis()} dictionary, run the request
           
           Arguments:
               sims        {name: sim()} dictionary of simulation names to simulation functions
               vis         {name: vis()} dictionary of visualization names to visualization functions
               store       {name: data} dictionary to write as additional data (optional)
        """

        if store is not None:
            with h5py.File(self.filepath, 'a') as f:
                if 'store' in f:
                    del f['store']
                for name,value in store.items():
                    f[f'store/{name}'] = value

        with h5py.File(self.filepath, 'a') as f:
            for name,sim in sims.items():
                if self.args.action in ['sim', 'both'] or name not in f:
                    if self.args.sims is not None and name not in self.args.sims:
                        continue

                    self.request(name)
                    print(f"Running simulation '{name}'")
                    symbols = sim()
                    if not isinstance(symbols,dict):
                        raise ValueError(f"simulation '{name}' needs to return a dictionary of symbols")
                    self.write(symbols, name)

        if self.args.action in ['vis', 'both']:
            print("Visualizing data...")
            for name,func in vis.items():
                func()



if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    ### Setup
    filepath = 'temp.h5'
    job = sim_and_vis(filepath)

    ### Fast, shared code goes here
    x = np.linspace(0,1,10)

    ### Slow, sim-only code goes here and relevant data is written to file
    def sim1():
        y = x**2
        return {'y': y**2}

    def sim2():
        z = x**2
        return {'z': z**3}

    ### Process/Visualize data here after loading symbols from file
    def vis():
        sim = job.read()
        plt.plot(x,sim.sim1.y)
        plt.plot(x,sim.sim2.z)
        plt.show()

    ### execute
    job.execute({'sim1': sim1, 'sim2': sim2}, {'vis': vis}, store={'x': x})
