from Utilities.Printable import Printable
from DataStructures.Nodeset import Nodeset

class Comparator(Printable):

    def __init__(self, runs):

        super().__init__('Comparator')

        self._runs = runs
        self._meshes = [run.mesh for run in self._runs]
        self._ele_ts = [run.elevation_timeseries for run in self._runs]
        self._vel_ts = [run.velocity_timeseries for run in self._runs]
        self._nodeset = Nodeset(self._meshes)

    def compare_elevation_timeseries(self, comparison):

        # Make sure all elevation timeseries datasets are loaded
        for ts in self._ele_ts:

            if ts is not None:

                ts.load()

            else:

                self.message('WARNING: ADCIRC run missing elevation timeseries')




