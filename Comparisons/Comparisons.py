from Utilities.Printable import Printable
from abc import abstractmethod
import numpy as np

class Comparison(Printable):

    def __init__(self, name):

        print('Calling Comparison constructor')
        super().__init__(name)

        self._start = None
        self._interval = None
        self._end = None

    def set_interval(self, start, interval, end):

        self._start = start
        self._interval = interval
        self._end = end

class BaselineComparison(Comparison):

    def __init__(self, name):

        super().__init__(name)

    @abstractmethod
    def next(self, baseline, data):
        """Passes the next dataset for processing"""

class CumulativeComparison(Comparison):

    def __init__(self, name):

        super().__init__(name)

    @abstractmethod
    def finalize(self):
        """Called once all data has be passed to the Comparison"""


class AverageDifference(BaselineComparison, CumulativeComparison):

    def __init__(self):

        super().__init__('Average Difference')

        self._cumulative = None
        self._num_datasets = 0

    def next(self, baseline, data):
        pass

    def finalize(self):

        pass
