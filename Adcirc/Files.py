import os
import numpy as np
from DataStructures.Datatypes import *
from Utilities.Printable import Printable

class File(Printable):

    def __init__(self, file, name=None):

        super().__init__(name or file.split(os.sep)[-1])

        try:

            self.f = open(file, 'rb')

        except IOError:

            print('Error: Cannot open file:', file)

class Fort14(File):

    def __init__(self, file):

        super().__init__(file, 'Mesh (fort.14)')

        self._ll = None
        self._ur = None

        self.header = self.f.readline()
        dat = self.f.readline().split()
        self.num_elements = int(dat[0])
        self.num_nodes = int(dat[1])

        self._nodes = np.empty((self.num_nodes, 2), dtype=np.float64)
        self._elements = np.empty((self.num_elements, 3), dtype=np.uint32)

        nn_to_ni = dict()

        self.message('Reading {} nodes'.format(self.num_nodes))

        for n in range(self.num_nodes):

            dat = self.f.readline().split()
            nn_to_ni[int(dat[0])] = n
            self._nodes[n, 0] = float(dat[1])
            self._nodes[n, 1] = float(dat[2])

        self.message('Reading {} elements'.format(self.num_elements))

        for e in range(self.num_elements):

            dat = self.f.readline().split()

            self._elements[e, 0] = nn_to_ni[int(dat[2])]
            self._elements[e, 1] = nn_to_ni[int(dat[3])]
            self._elements[e, 2] = nn_to_ni[int(dat[4])]

    def node_coordinates(self):

        return self._nodes

    def element_coordinates(self):
        """Returns ndarray of coordinates that comprise all elements.

        Returns numpy array of shape (# elements, 3, 2) where each element in the array
        is a list of nodes, and each node is a list of x, y coordinates.
        """

        self.message('Generating element coordinates')
        return self._nodes[self._elements]

    def centroids(self):
        """Returns ndarray of centroids of elements.

        Returns numpy array of shape (# elements, 2) where each element in the array
        is a list of x, y coordinates
        """

        self.message('Generating centroids')
        return np.divide(np.sum(self.element_coordinates(), axis=1), 3.0)

    def bounds(self):

        if self._ll is None or self._ur is None:

            self.message('Calculating bounding box')
            self._ll = self._nodes.min(axis=0)
            self._ur = self._nodes.max(axis=0)
            self.message('Bounding box:', self._ll, self._ur)

        return self._ll, self._ur

    def lower_left_bound(self):

        return self.bounds()[0]

    def upper_right_bound(self):

        return self.bounds()[1]