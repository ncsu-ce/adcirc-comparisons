from Utilities.Printable import Printable
from array import array
from collections import defaultdict
import numpy as np

class Nodeset(Printable):

    def __init__(self, files):

        super().__init__('NetCDF Nodeset')

        self._files = files
        self._common_nodes = None
        self._common_indices = None

        self._find_common_nodes()

    def common_nodes(self):

        return self._common_nodes

    def common_indices(self, index):

        return self._common_indices[:,index]

    def num_nodes(self):

        return self._common_nodes.shape[0]

    def _find_common_nodes(self):

        self.message('Finding common nodes')

        nodal_indices = defaultdict(lambda: array('l', [-1] * len(self._files)))

        for file_index, f in enumerate(self._files):

            keys = f.variables.keys()

            if 'x' in keys and 'y' in keys:

                x = f.variables['x']
                y = f.variables['y']

                if x.shape == y.shape:

                    coordinates = np.empty((x.shape[0], 2))
                    coordinates[:,0] = x[:]
                    coordinates[:,1] = y[:]

                    for index, coord in enumerate(coordinates):

                        nodal_indices[coord.tobytes()][file_index] = index


        common_nodes = dict()

        for key, indices in nodal_indices.items():

            if indices.count(-1) == 0:

                common_nodes[key] = indices

        num_common_nodes = len(common_nodes)
        self._common_nodes = np.empty((num_common_nodes, 2), dtype=np.float64)
        self._common_indices = np.empty((num_common_nodes, len(self._files)), dtype=np.uint32)

        for index, (key, indices) in enumerate(common_nodes.items()):

            self._common_nodes[index] = np.fromstring(key, np.float64, 2)
            self._common_indices[index] = indices

        self.message('Found {} common nodes'.format(num_common_nodes))