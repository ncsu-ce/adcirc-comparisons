from Utilities.Printable import Printable
from NC.Nodeset import Nodeset
from NC.Timestepper import CommonTimesteps
from scipy.io import netcdf as nc
import numpy as np

class Comparator(Printable):

    def __init__(self, baseline, files):

        super().__init__('NetCDF Comparator')

        self._baseline = nc.netcdf_file(baseline, 'r')
        self._comps = [nc.netcdf_file(f, 'r') for f in self._cleanse_files(files)]
        self._files = [self._baseline] + self._comps
        self._nodeset = Nodeset([baseline]+files)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        # Destroy any references to netcdf variables
        self._nodeset = None
        self._baseline = None
        self._comps = None

        # Close all files
        self.message('Closing all netcdf files')

        for f in self._files:
            f.close()

    def average_difference(self, variable):

        self.message('Calculating average difference for variable \'{}\''.format(variable))

        # Load the variable from every file
        times = self._load_variable('time')
        variables = self._load_variable(variable)
        baseline = variables[0]
        comps = variables[1:]

        # Ensure variable present in all files
        if variables is None:
            self.message('Variable {} missing from one of the data files'.format(variable))
            return

        # Get the common nodes and nodal indices
        common_nodes, common_indices = self._nodeset.common_nodes()
        print(common_nodes)
        print(common_indices)
        print(common_nodes.shape)
        print(baseline.shape)

        # Create accumulators
        cumulative_difference = np.zeros((common_nodes.shape[0], len(comps)), dtype=np.float64)
        cumulative_values = np.zeros((common_nodes.shape[0], len(comps)), dtype=np.uint32)

        timestepper = CommonTimesteps(times)
        while timestepper.has_next_timestep():

            # Get the index of the current timestep for each dataset
            time, indices = timestepper.next_timestep()

            # Get the baseline values
            baseline_values = baseline[indices[0],:]

            # Get the values from all others
            comp_values = [comp[indices[i]] for i, comp in enumerate(comps)]
            print(baseline_values.shape, list(map(lambda c: c.shape, comp_values)))

            # Loop through each file and calculate difference
            for c, comp_value in enumerate(comp_values):

                # Calculate difference (array subtraction)
                difference = baseline_values - comp_value

                # Add to accumulators
                np.add(cumulative_difference[:,c], difference, out=cumulative_difference[:,c])
                np.add(cumulative_values[:,c], 1, out=cumulative_difference[:,c])

            # Calculate averages
            average_difference = np.empty(cumulative_difference.shape, dtype=np.float64)
            np.divide(cumulative_difference, cumulative_values, out=average_difference)

            print(average_difference)

            # print(time, indices)

    def _load_variable(self, variable):

        for f in self._files:
            if variable not in f.variables.keys():
                return None

        return [f.variables[variable] for f in self._files]

    def _cleanse_files(self, files):

        cleansed = []

        for file in files:

            with nc.netcdf_file(file, 'r') as f:

                if 'time' in f.variables.keys():

                    cleansed.append(file)

                else:

                    self.warning('{} does not contain time variable, it will be excluded'.format(file))

                f.close()

        return cleansed

