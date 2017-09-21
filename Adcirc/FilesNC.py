from Utilities.Printable import Printable
from scipy.io import netcdf

class Fort63NC(Printable):

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._times = None
        self._f.close()

    def __init__(self, file_path):

        super().__init__('NetCDF File (fort.63)')

        self._f = netcdf.netcdf_file(file_path, 'r')
        self._times = self._f.variables['time']

    def print_some(self, variable):

        if variable in self._f.variables.keys():
            v = self._f.variables[variable]
            l = v.shape[0]
            self.message('The first few values from variable {} - {}'.format(variable, v.shape))
            for i in range(10):
                self.message('{}\t{}'.format(i, v[i]))
            for i in range(l-10, l):
                self.message('{}\t{}'.format(i, v[i]))
            v = None

    def print_everything(self):

        keys = dir(self._f)
        for key in keys:
            if key[0] != '_' and key != 'variables':
                value = getattr(self._f, key)
                self.message('{:25} {}'.format(key, str(value)))

    def print_variables(self):

        keys = self._f.variables.keys()
        for key in keys:
            value = self._f.variables[key]
            shape = value.shape
            units = value.typecode()
            size = value.itemsize()

            i = 0
            suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
            sz = size
            if len(shape) > 0:
                sz *= shape[0]
                if len(shape) > 1:
                    sz *= shape[1]
                while sz >= 1024 and i < len(suffixes)-1:
                    sz /= 1024.0
                    i += 1

            hr_size = '{:7.2f} '.format(sz) + suffixes[i]

            self.message('{:15} {:15} {:4} {}'.format(str(key), str(shape), str(units)+str(size), hr_size))

    def num_dimensions(self):

        return self._ndims

    def num_datasets(self):

        return self._num_datasets

    def time(self):

        return self._times

    def data(self):

        return self._data