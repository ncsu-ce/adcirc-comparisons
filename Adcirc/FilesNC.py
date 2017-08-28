from netCDF4 import Dataset
from scipy.io import netcdf
import numpy as np

class Fort63NC:

    def __init__(self, file_path):

        try:
            f = netcdf.netcdf_file(file_path)
            print(f.variables.keys())

            time = f.variables['time']
            x = f.variables['x']
            y = f.variables['y']
            z = f.variables['depth']
            ele_ts = f.variables['zeta']
            print(time.units)
            print(len(time[:]))
            print(x[:])
            print(y[:])
            print(z[:])
            print(np.mean(ele_ts[:], axis=0))

        except RuntimeError:

            print('Error.')

        finally:

            time = None
            x = None
            y = None
            z = None
            ele_ts = None