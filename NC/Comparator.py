from Utilities.Printable import Printable
from NC.Nodeset import Nodeset
from NC.Timestepper import CommonTimesteps
from scipy.io import netcdf as nc
from functools import reduce

class Comparator(Printable):

    def __init__(self, files):

        super().__init__('NetCDF Comparator')

        self._files = [nc.netcdf_file(f, 'r') for f in self._cleanse_files(files)]
        self._nodeset = Nodeset(files)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        # Destroy any references to netcdf variables
        self._nodeset = None

        self.message('Closing all netcdf files')

        for f in self._files:
            f.close()

    def average_difference(self, variable):

        self.message('Calculating average difference for variable \'{}\''.format(variable))

        # Load the variable from every file
        times = self._load_variable('time')
        variables = self._load_variable(variable)

        # Ensure variable present in all files
        if variables is None:
            self.message('Variable {} missing from one of the data files'.format(variable))
            return

        timestepper = CommonTimesteps(times)
        while timestepper.has_next_timestep():

            # Get the index of the current timestep for each dataset
            time, indices = timestepper.next_timestep()
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

