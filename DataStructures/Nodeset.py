from Utilities.Printable import Printable
import numpy as np
import scipy.spatial as sp
from array import array
from collections import defaultdict, Counter

class Nodeset(Printable):

    def __init__(self, meshes, include_uncommon_nodes=True):

        super().__init__('Nodeset')

        self._meshes = meshes
        self._num_meshes = len(meshes)
        self._ll = None
        self._ur = None

        self._common_nodes = None
        self._uncommon_nodes = None

        self._calculate_bounds()

        if include_uncommon_nodes:
            self._find_all_nodes()
        else:
            self._find_only_common_nodes()

    def _find_all_nodes(self):

        self.message('Finding all nodes')
        self._common_nodes = set()
        self._uncommon_nodes = dict()
        appears = defaultdict(lambda: array('b', [0] * self._num_meshes))

        for m in range(self._num_meshes):

            nodal_coordinates, in_range = self._coordinates_in_range(m)

            # If the node appears, flip the mesh index to true
            for n in range(nodal_coordinates.shape[0]):

                if in_range[n]:

                    appears[nodal_coordinates[n].tobytes()][m] = 1

        for key, counts in appears.items():

            if counts.count(1) == self._num_meshes:

                self._common_nodes.add(key)

            else:

                self._uncommon_nodes[key] = counts

        self.message('Found {} common nodes'.format(len(self._common_nodes)))
        self.message('Found {} uncommon nodes'.format(len(self._uncommon_nodes)))


        self.message('Finding common elements')
        common_centroids = 0
        uncommon_centroids = 0
        centroid_indices = defaultdict(lambda: array('l', [-1] * self._num_meshes))

        for m in range(self._num_meshes):

            centroids, in_range = self._centroids_in_range(m)

            # If the centroid appears, keep track of the index
            for c in range(centroids.shape[0]):

                if in_range[c]:

                    centroid_indices[centroids[c].tobytes()][m] = c

        centroid_dicts = [dict()] * self._num_meshes

        for key, indices in centroid_indices.items():

            if indices.count(-1) != 0:

                uncommon_centroids += 1

                for m in range(self._num_meshes):

                    if indices[m] != -1:

                        centroid_dicts[m][key] = indices[m]

            else:

                common_centroids += 1

        self.message('Found {} common elements'.format(common_centroids))
        self.message('Found {} uncommon elements'.format(uncommon_centroids))


        self.message('Building searchable data structure to compute overlaps')
        centroid_arrays = [None] * self._num_meshes

        for m in range(self._num_meshes):

            centroid_dict = centroid_dicts[m]
            num_centroids = len(centroid_dict)
            centroid_arrays[m] = np.empty((num_centroids, 2), dtype=np.float64)

            for i, key in enumerate(centroid_dict.keys()):

                centroid_arrays[m][i] = np.fromstring(key, np.float64, 2)

        centroid_trees = [None] * self._num_meshes

        for m in range(self._num_meshes):

            centroid_trees[m] = sp.cKDTree(centroid_arrays[m])

        self.message('Done')

    def _find_only_common_nodes(self):

        self.message('Finding common nodes')

        self._common_nodes = set()
        counter = Counter()

        for m in range(self._num_meshes):

            nodal_coordinates, in_range = self._coordinates_in_range(m)

            # Count number of times each node appears
            for n in range(nodal_coordinates.shape[0]):

                if in_range[n]:

                    counter[nodal_coordinates[n].tobytes()] += 1

        # Only include nodes that are in every mesh
        for key, counts in counter.items():

            if counts == self._num_meshes:

                self._common_nodes.add(key)

        self.message('Found {} common nodes'.format(len(self._common_nodes)))

    def _calculate_bounds(self):

        self.message('Calculating bounding box')
        lls = np.empty((self._num_meshes, 2))
        urs = np.empty((self._num_meshes, 2))

        for m in range(self._num_meshes):
            lls[m] = self._meshes[m].lower_left_bound()
            urs[m] = self._meshes[m].upper_right_bound()

        self._ll = lls.max(axis=0)
        self._ur = urs.min(axis=0)
        self.message('Bounding box:', self._ll, self._ur)

    def _coordinates_in_range(self, _mesh_index):

        nodal_coordinates = self._meshes[_mesh_index].node_coordinates()
        return nodal_coordinates, self._array_in_range(nodal_coordinates)

    def _centroids_in_range(self, _mesh_index):

        centroids = self._meshes[_mesh_index].centroids()
        return centroids, self._array_in_range(centroids)

    def _array_in_range(self, arr):

        return np.all(
            np.logical_and(
                self._ll <= arr,
                self._ur >= arr
            ), axis=1
        )
