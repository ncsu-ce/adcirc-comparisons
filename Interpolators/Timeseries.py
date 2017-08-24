from Utilities.Printable import Printable
import numpy as np

class TimeseriesInterpolator(Printable):

    def __init__(self, fortND):

        super().__init__('TS Interpolator')

        self._f = fortND
        self._times = self._f.times()
        self._data = self._f.data()
        self._num_datasets = self._f.num_datasets()
        self._num_dimensions = self._f.num_dimensions()
        self._null_value = -99999.0

    def timestep(self, model_time):

        t, d = self._get_interp_timesteps(model_time)
        mask = d == self._null_value

        if t.shape[0] == 1:
            if self._num_dimensions > 1:
                return d, np.any(mask, axis=1)
            else:
                return d, mask

        r = (model_time - t[0]) / (t[1] - t[0])
        l = 1.0 - r

        if self._num_dimensions > 1:
            return l*d[0] + r*d[1], np.any(np.any(mask, axis=0), axis=1)
        else:
            return l*d[0] + r*d[1], np.any(mask, axis=0)

    def _get_interp_timesteps(self, model_time):

        # Check for boundary cases first
        if model_time == self._times[0]:
            return self._times[0:1], self._data[0]
        if model_time == self._times[-1]:
            return self._times[-1:], self._data[-1]

        # Find where the time would be inserted
        i = np.searchsorted(self._times, model_time)

        # If it's the beginning or end, we'd have to extrapolate
        if i == 0:
            self.message('ERROR: Cannot interpolate before first timestep')
            self.message('First timestep occurs at {} seconds'.format(self._times[0]))
            exit()
        elif i == self._num_datasets:
            self.message('ERROR: Cannot interpolate past final timestep')
            self.message('Last timestep occurs at {} seconds'.format(self._times[-1]))
            exit()

        l = self._times[i - 1]
        r = self._times[i]

        if l == model_time:
            return self._times[i-1:i], self._data[i-1]
        if r == model_time:
            return self._times[i:i+1], self._data[i]

        return self._times[i-1:i+1], self._data[i-1:i+1]