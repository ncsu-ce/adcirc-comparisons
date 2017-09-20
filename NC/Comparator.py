from Utilities.Printable import Printable
from NC.Nodeset import Nodeset
from scipy.io import netcdf as nc
from functools import reduce

class Comparator(Printable):

    def __init__(self, files):

        super().__init__('NetCDF Comparator')

        self._files = self._cleanse_files(files)
        self._nodeset = Nodeset(files)

    def average_difference(self, variable):

        # Load the variable from every file

        files = open_files(self._files)

        for f in files:

            if variable not in f.variables.keys():

                self.message('{} variable not in file {}'.format(variable, f.filename))
                close_files(files)
                return

        times = [f.variables['time'] for f in files]
        variables = [f.variables[variable] for f in files]



        # Start timestepping



        # Clean up
        times = None
        variables = None
        close_files(files)

    @staticmethod
    def _cleanse_files(files):

        cleansed = []

        for file in files:

            with nc.netcdf_file(file, 'r') as f:

                if 'time' in f.variables.keys():

                    cleansed.append(file)

                f.close()

        return cleansed


def open_files(files):
    return [nc.netcdf_file(f, 'r') for f in files]


def close_files(files):
    for f in files:
        f.close()

def first_common_timestep(times):

    indices = [0] * len(times)
    values = [times[i][indices[i]] for i in range(len(times))]
    mindex = values.index(min(values))

    while not all(t == values[0] for t in values):

        if indices[mindex] + 1 >= len(times[mindex]):

            return None

        indices[mindex] += 1
        values[mindex] = times[mindex][indices[mindex]]
        mindex = values.index(min(values))

    return indices

def next_common_timestep(times, indices):

    next_indices = [i+1 for i in indices]

    for i in range(len(times)):
        if next_indices[i] >= len(times[i]):
            return None

    next_values = [times[i][next_indices[i]] for i in range(len(times))]
    next_mindex = next_values.index(min(next_values))

    indices[next_mindex] += 1
    values = [times[i][indices[i]] for i in range(len(times))]
    mindex = values.index(min(values))

    while not all(t == values[0] for t in values):

        if indices[mindex] + 1 >= len(times[mindex]):
            return None

        indices[mindex] += 1
        values[mindex] = times[mindex][indices[mindex]]
        mindex = values.index(min(values))

    return indices


