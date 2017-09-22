from Utilities.Printable import Printable
from NC.Nodeset import Nodeset
from NC.Timestepper import CommonTimesteps
from NC.Data import Accumulators, Variable
from scipy.io import netcdf as nc
import numpy as np

class Comparator(Printable):

    def __init__(self, baseline, files):

        super().__init__('NetCDF Comparator')

        # The baseline against which all comparisons will be performed
        baseline = self._cleanse_file(baseline)
        if baseline is None:
            self.error('There is no time variable in the baseline file, exiting')
            exit(1)
        self._base = nc.netcdf_file(baseline, 'r')

        # The list of files to be compared to the baseline
        self._comp = [nc.netcdf_file(f, 'r') for f in self._cleanse_files(files)]
        if len(self._comp) == 0:
            self.error('None of the provided files contain a time variable, exiting')
            exit(1)

        # The list of all runs, baseline and comparisons included
        self._runs = [self._base] + self._comp

        # The nodeset at which to calculate comparisons
        self._nodeset = Nodeset(self._runs)

        # The time variable for every run
        self._times = [f.variables['time'] for f in self._runs]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        # Destroy any references to netcdf variables
        self._nodeset = None
        self._base = None
        self._comp = None
        self._times = None

        # Close all files
        self.message('Closing all netcdf files')

        for f in self._runs:
            f.close()

    def avg_difference(self, variable):

        self.message('Calculating average difference for variable \'{}\''.format(variable))

        # Retrieve the baseline and comparison variables
        base, comp = self._load_variable(variable)

        # Create the accumulators
        accumulators = Accumulators(len(comp), self._nodeset.num_nodes(), np.float64)

        # Create the timestepper
        timestepper = CommonTimesteps(self._times)

        # Loop and calculate
        while timestepper.has_next_timestep():

            # Get the next timestep
            model_time, time_indices = timestepper.next_timestep()
            tindex_base = time_indices[0]
            tindex_comp = time_indices[1:]

            self.message_sameline('Calculating average difference at time {}'.format(model_time))

            # Get the baseline values
            val_base = base.timestep(tindex_base)

            for c, cmp in enumerate(comp):

                # Get the comparison value
                val_comp = cmp.timestep(tindex_comp[c])

                # Calculate the absolute value of the difference
                difference = np.abs(val_base - val_comp)

                # Add to the appropriate accumulator
                accumulators[c].add(difference)

        self.finish_sameline()

        # Calculate the average
        return [acc.average() for acc in accumulators]

    def _cleanse_file(self, file):

        with nc.netcdf_file(file, 'r') as f:

            if 'time' in f.variables.keys():

                f.close()
                return file

            f.close()
            self.warning('{} does not contain time variable, it will be excluded'.format(file))

    def _cleanse_files(self, files):

        cleansed = []

        for file in files:

            clean = self._cleanse_file(file)

            if clean is not None:

                cleansed.append(clean)

        return cleansed

    def _load_variable(self, variable):

        # Check that the variable exists in all files
        for f in self._runs:
            if variable not in f.variables.keys():
                self.error('Variable \'{}\' missing from file, exiting')
                exit(1)

        # Create the baseline variable
        var = self._base.variables[variable]
        nodal_indices = self._nodeset.common_indices(0)
        base = Variable(var, nodal_indices)

        # Create each comparison variable
        comp = []
        for i, _comp in enumerate(self._comp):
            var = _comp.variables[variable]
            nodal_indices = self._nodeset.common_indices(i+1)
            comp.append(Variable(var, nodal_indices))

        return base, comp