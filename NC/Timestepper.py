from abc import ABCMeta, abstractmethod
from Utilities.Printable import Printable

class Timestepper(Printable, metaclass=ABCMeta):

    def __init__(self, name=None):

        super().__init__('Timestepper' if name is None else name)

    @abstractmethod
    def has_next_timestep(self):
        """Returns true or false depending on whether or not there is another timestep available"""

    @abstractmethod
    def next_timestep(self):
        """Returns the next timestep (implementation dependent) if there is one, None otherwise"""


class CommonTimesteps(Timestepper):

    def __init__(self, time_arrays):

        super().__init__('Common Timesteps')

        self._arrays = time_arrays
        self._indices = [0] * len(time_arrays)
        self._has_next = True

        # Ensure data available to initialize
        for a in self._arrays:
            if a.shape[0] == 0:
                self._has_next = False
                return

        # Initialize values
        self._num_arrays = len(self._arrays)
        self._array_lengths = [a.shape[0] for a in self._arrays]
        self._values = [self._arrays[i][index] for i, index in enumerate(self._indices)]

        # Inform
        print(self._array_lengths)
        for i in range(len(self._array_lengths)):
            self.message('Timestep range ({}, {})'.format(self._arrays[i][0], self._arrays[i][-1]))

        # Advance until we find the first common timestep
        while not self._are_common():

            # Attempt to advance
            if not self._advance():

                break

    def has_next_timestep(self):

        return self._has_next

    def next_timestep(self):

        current_value = self._values[0]
        current_indices = self._indices

        self._advance()

        while not self._are_common():

            if not self._advance():

                break

        return current_value, current_indices

    def _advance(self):

        # If the values are all the same, advance all arrays by one
        if self._are_common():

            # Determine what the next index would be for all of the arrays
            self._indices = [index + 1 for index in self._indices]

            # Make sure data actually exists at all of these subsequent indices
            for i in range(self._num_arrays):
                if self._indices[i] >= self._array_lengths[i]:
                    return self._cleanup()

            # Set the values
            self._values = [self._arrays[i][index] for i, index in enumerate(self._indices)]

        # If the values are not the same, only advance the array with the
        # current minimum timestep value
        else:

            # Determine the index of the minimum array value
            mindex = self._values.index(min(self._values))

            # Advance that array index
            self._indices[mindex] += 1

            # Make sure data exists at that index
            if self._indices[mindex] >= self._array_lengths[mindex]:
                return self._cleanup()

            # Advance the value
            self._values[mindex] = self._arrays[mindex][self._indices[mindex]]

        return True


    def _are_common(self):

        return all(value == self._values[0] for value in self._values)

    def _cleanup(self):

        self._has_next = False
        self._arrays = None
        return False