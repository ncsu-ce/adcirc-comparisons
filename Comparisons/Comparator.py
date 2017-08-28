from Utilities.Printable import Printable
from DataStructures.Nodeset import Nodeset
from Interpolators.Timeseries import TimeseriesInterpolator
import numpy as np

class Comparator(Printable):

    def __init__(self, runs):

        super().__init__('Comparator')

        self._runs = runs
        # self._meshes = [run.mesh for run in self._runs]
        # self._ele_ts = [run.elevation_timeseries for run in self._runs]
        # self._vel_ts = [run.velocity_timeseries for run in self._runs]
        # self._nodeset = Nodeset(self._meshes)

    def compare_elevation_timeseries(self, baseline, runs):

        if baseline.elevation_timeseries is not None:

            for run in runs:

                if run.elevation_timeseries is None:

                    self.message('ERROR: ADCIRC run is missing elevation timeseries')
                    exit()


            # Create the nodeset
            meshes = [baseline.mesh] + [run.mesh for run in runs]
            nodeset = Nodeset(meshes, False)
            common_nodes, common_indices = nodeset.common_nodes()

            # Build timeseries
            ele_ts = [baseline.elevation_timeseries] + [run.elevation_timeseries for run in runs]
            for ts in ele_ts: ts.load()
            timeseries = [TimeseriesInterpolator(ts) for ts in ele_ts]

            # Use the times of the baseline
            times = baseline.elevation_timeseries.times()

            # Accumulators
            cumulative_error = np.zeros((common_nodes.shape[0], len(runs)), dtype=np.float64)
            cumulative_values = np.zeros((common_nodes.shape[0], len(runs)), dtype=np.uint32)
            maximum_error = np.zeros((common_nodes.shape[0], len(runs)), dtype=np.float64)

            self.message('Starting timestepping')

            for i, t in enumerate(times):

                self.message_sameline('Computing errors for timestep {}/{}'.format(i+1, len(times)))

                # Get the baseline data
                baseline_data_full, baseline_mask_full = timeseries[0].timestep(t)
                baseline_data = baseline_data_full[common_indices[:,0]]
                baseline_mask = baseline_mask_full[common_indices[:,0]]

                # Loop through each mesh
                for m in range(len(runs)):

                    data_full, mask_full = timeseries[1+m].timestep(t)
                    data = data_full[common_indices[:,1+m]]
                    mask = mask_full[common_indices[:,1+m]] | baseline_mask
                    error = np.abs(data-baseline_data)

                    np.add(cumulative_error[:,m], error, out=cumulative_error[:,m], where=~mask)
                    np.add(cumulative_values[:,m], 1, out=cumulative_values[:,m], where=~mask)
                    np.maximum(maximum_error[:,m], error, out=maximum_error[:,m], where=~mask)

            self.finish_sameline()

            results_mask = cumulative_values != 0
            average_error = np.empty(cumulative_error.shape, dtype=np.float64)
            np.divide(cumulative_error, cumulative_values, out=average_error, where=results_mask)
            average_error[~results_mask] = -99999.0

            return common_nodes, average_error, maximum_error

