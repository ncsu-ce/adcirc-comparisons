from Utilities.Printable import Printable
import numpy as np

def linear_interpolator(a, b):

    def interpolate(p):

        l = 1.0 - p
        r = p

        return l*a + r*b

    return interpolate

class Variable(Printable):

    def __init__(self, nc_variable, nodal_indices=None, null_val=None):
        """ An ADCIRC variable from a NetCDF file

        The nc_variable will be of shape (#ts, #nodes).

        :param nc_variable: the netcdf_variable object from the netcdf file
        :param nodal_indices: (Optional) The nodal indices to use when accessing data
        """

        super().__init__('NetCDF Variable')

        self._var = nc_variable
        self._nodal_indices = nodal_indices
        self._null_val = null_val

        self.message('Variable created with shape', nc_variable.shape, nodal_indices.shape)

    def timestep(self, *index):

        ts = None

        if self._nodal_indices is None:

            ts = self._timestep_simple(*index)

        elif isinstance(self._nodal_indices, (list, np.ndarray)):

            ts = self._timestep_indexed(*index)

        if ts is not None:

            if self._null_val is not None:

                mask = ts == self._null_val
                return ts, mask

            return ts

    def _timestep_simple(self, *index):

        if len(index) == 1:

            return self._var[index]

        if len(index) == 2:

            l = self._var[index[0]]
            r = self._var[index[1]]
            return linear_interpolator(l, r)

    def _timestep_indexed(self, *index):

        if len(index) == 1:

            return self._var[index, self._nodal_indices]

        if len(index) == 2:

            l = self._var[index[0], self._nodal_indices]
            r = self._var[index[1], self._nodal_indices]
            return linear_interpolator(l, r)


class Accumulator(Printable):

    def __init__(self, num_values, dtype):

        super().__init__('Accumulator')

        self._acc = np.zeros((num_values,), dtype=dtype)
        self._cnt = np.zeros((num_values,), dtype=np.uint32)

    def add(self, values, mask=None):

        if mask is None:

            np.add(self._acc, values, out=self._acc)
            np.add(self._cnt, 1, out=self._cnt)

        else:

            np.add(self._acc, values, out=self._acc, where=~mask)
            np.add(self._cnt, 1, out=self._cnt, where=~mask)


    def average(self, null_value=-99999):

        # Create a mask where values are equal to zero
        mask = self._cnt != 0

        # Create variable to hold averages
        avg = np.empty(self._acc.shape, dtype=np.float64)

        # Calculate averages where values are not equal to zero
        np.divide(self._acc, self._cnt, out=avg, where=mask)

        # Fill everywhere else with null value
        avg[~mask] = null_value

        return avg

class Accumulators:

    def __init__(self, count, shape, dtype):

        self._accumulators = [None] * count
        self._index = 0

        for i in range(count):

            self._accumulators[i] = Accumulator(shape, dtype)

    def __iter__(self):
        return self

    def __next__(self):
        if self._index == len(self._accumulators):
            raise StopIteration
        index = self._index
        self._index += 1
        return self._accumulators[index]

    def __getitem__(self, item):

        return self._accumulators[item]