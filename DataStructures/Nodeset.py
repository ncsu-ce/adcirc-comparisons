from Utilities.Printable import Printable
import numpy as np
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

        self.message('Finding all nodes nodes')
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
        centroid_counter = Counter()
        common_centroids = 0
        uncommon_centroids = set()
        for m in range(self._num_meshes):

            centroids, in_range = self._centroids_in_range(m)

            for c in range(centroids.shape[0]):

                if in_range[c]:

                    centroid_counter[centroids[c].tobytes()] += 1

        for key, counts in centroid_counter.items():

            if counts == self._num_meshes:

                common_centroids += 1

            else:

                uncommon_centroids.add(key)

        uncommon_centroids_array = np.empty((len(uncommon_centroids), 2))

        for i, key in enumerate(uncommon_centroids):

            uncommon_centroids_array[i] = np.fromstring(key, np.float64, 2)

        self.message('Found {} common elements'.format(common_centroids))
        self.message('Found {} uncommon elements'.format(len(uncommon_centroids)))

        # We can't use np.isin because it doesn't operate on 2D arrays. Let's explort
        # what we can do with custom data types...
        for m in range(self._num_meshes):

            centroids, in_range = self._centroids_in_range(m)

            ### WARNING: GARBAGE
            searchable_centroids = np.isin(centroids[in_range], uncommon_centroids_array, True)

            print(searchable_centroids)



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
