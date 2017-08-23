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

    def _find_common_and_uncommon_nodes(self):
        """Returns a set of common nodes, a set of uncommon nodes, and a list of uncommon nodesets

        The set of common nodes is every node that falls into all meshes. The set of uncommon
        nodes is every node that is missing from at least one mesh. The list of uncommon
        nodesets is the set of nodes missing from each mesh.
        """

        self.message('Finding common and uncommon nodes')
        common_nodes = set()
        uncommon_nodes = set()
        uncommon_nodesets = [set() for _ in range(self._num_meshes)]
        appears = defaultdict(lambda: array('b', [0] * self._num_meshes))

        # Build a binary array for each node. The bit at each index will indicate
        # whether the node appears in the mesh.
        for m in range(self._num_meshes):

            nodal_coordinates, in_range = self._coordinates_in_range(m)

            for n in range(nodal_coordinates.shape[0]):

                if in_range[n]:

                    appears[nodal_coordinates[n].tobytes()][m] = 1

        # If the number of times a node appears is equal to the number of meshes,
        # then the node is a common node. Otherwise, keep track of which meshes
        # the node does not fall into
        for key, in_mesh in appears.items():

            if in_mesh.count(1) == self._num_meshes:

                common_nodes.add(key)

            else:

                uncommon_nodes.add(key)

                for m in range(self._num_meshes):

                    if in_mesh[m] == 0:

                        uncommon_nodesets[m].add(key)

        self.message('{} nodes fall into all meshes'.format(len(common_nodes)))
        self.message('{} nodes are missing from at least one mesh'.format(len(uncommon_nodes)))
        for m in range(self._num_meshes):
            self.message('{} nodes missing from mesh {}'.format(len(uncommon_nodesets[m]), m))

        return common_nodes, uncommon_nodes, uncommon_nodesets

    def _build_searches(self):
        """Returns a list of searchable data structures, one for each mesh, as well as element index dictionaries

        Each searchable data structure (in this case, np.cKDTree) will contain
        centroids for all elements that fall into the nodeset range and are not
        common to all meshes. Each dictionary maps from a centroid coordinate
        to an element number.
        """

        self.message('Finding common and uncommon elements')

        common_centroids = 0
        uncommon_centroids = 0
        centroid_indices = defaultdict(lambda: array('l', [-1] * self._num_meshes))

        for m in range(self._num_meshes):

            centroids, in_range = self._centroids_in_range(m)

            for c in range(centroids.shape[0]):

                if in_range[c]:

                    centroid_indices[centroids[c].tobytes()][m] = c

        centroid_dicts = [dict() for _ in range(self._num_meshes)]

        for key, indices in centroid_indices.items():

            if indices.count(-1) == 0:

                common_centroids += 1

            else:

                uncommon_centroids += 1

                for m in range(self._num_meshes):

                    if indices[m] != -1:

                        centroid_dicts[m][key] = indices[m]

        self.message('{} elements fall into all meshes'.format(common_centroids))
        self.message('{} elements are missing from at least one mesh'.format(uncommon_centroids))
        self.message('Building element searches for each mesh')

        centroid_arrays = [None] * self._num_meshes
        centroid_searches = [None] * self._num_meshes

        for m in range(self._num_meshes):

            num_centroids = len(centroid_dicts[m])

            if num_centroids > 0:

                centroid_arrays[m] = np.empty((num_centroids, 2), dtype=np.float64)

                for index, key in enumerate(centroid_dicts[m].keys()):

                    centroid_arrays[m][index] = np.fromstring(key, np.float64, 2)

                centroid_searches[m] = sp.cKDTree(centroid_arrays[m])

        return centroid_searches, centroid_dicts


    def _find_element_overlaps(self, nodesets, centroid_searches, centroid_dicts):

        self.message('Precalculating barycentric coordinates for node/element overlaps')

        barycentric_indices = [dict() for _ in range(self._num_meshes)]
        barycentric_coordinates = [dict() for _ in range(self._num_meshes)]

        for m in range(self._num_meshes):

            num_nodes = len(nodesets[m])

            if centroid_searches[m] is not None:

                coordinates = set_to_coordinate_array(nodesets[m])
                centroid_indices = centroid_searches[m].query(coordinates)[1]
                element_indices = np.empty(num_nodes, dtype=np.uint32)

                for n in range(num_nodes):

                    closest_index = centroid_indices[n]
                    key = centroid_searches[m].data[closest_index].data.tobytes()
                    element_indices[n] = centroid_dicts[m][key]

                element_coordinates = self._meshes[m].element_coordinates(element_indices)
                bary, mask = barycentric(coordinates, element_coordinates)

                for n in range(num_nodes):

                    if mask[n]:

                        key = centroid_searches[m].data[centroid_indices[n]].data.tobytes()
                        element_index = element_indices[n]

                        barycentric_indices[m][key] = element_index
                        barycentric_coordinates[m][key] = bary[n]

            self.message('Mesh {} has {} calculable nodes'.format(m, len(barycentric_indices[m])))

        print(barycentric_coordinates)
        return barycentric_indices, barycentric_coordinates

    def _find_all_nodes(self):

        common_nodes, uncommon_nodes, uncommon_nodesets = self._find_common_and_uncommon_nodes()
        centroid_searches, centroid_dicts = self._build_searches()
        indices, coordinates = self._find_element_overlaps(uncommon_nodesets, centroid_searches, centroid_dicts)
        return

        # self.message('Finding all nodes')
        # self._common_nodes = set()
        # self._uncommon_nodes = dict()
        # uncommon_node_counts = [0] * self._num_meshes
        # appears = defaultdict(lambda: array('b', [0] * self._num_meshes))
        #
        # for m in range(self._num_meshes):
        #
        #     nodal_coordinates, in_range = self._coordinates_in_range(m)
        #
        #     # If the node appears, flip the mesh index to true
        #     for n in range(nodal_coordinates.shape[0]):
        #
        #         if in_range[n]:
        #
        #             appears[nodal_coordinates[n].tobytes()][m] = 1
        #             uncommon_node_counts[m] += 1
        #
        # for key, counts in appears.items():
        #
        #     if counts.count(1) == self._num_meshes:
        #
        #         self._common_nodes.add(key)
        #
        #     else:
        #
        #         self._uncommon_nodes[key] = counts
        #
        # self.message('Found {} common nodes'.format(len(self._common_nodes)))
        # self.message('Found {} uncommon nodes'.format(len(self._uncommon_nodes)))


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


        self.message('Building searchable data structures to compute overlaps')
        centroid_arrays = [None] * self._num_meshes
        centroid_trees = [None] * self._num_meshes

        for m in range(self._num_meshes):

            centroid_dict = centroid_dicts[m]
            num_centroids = len(centroid_dict)
            centroid_arrays[m] = np.empty((num_centroids, 2), dtype=np.float64)

            for i, key in enumerate(centroid_dict.keys()):

                centroid_arrays[m][i] = np.fromstring(key, np.float64, 2)

            centroid_trees[m] = sp.cKDTree(centroid_arrays[m])


        self.message('Precalculating barycentric coordinates')
        barycentric = [dict()] * self._num_meshes
        for key, counts in self._uncommon_nodes:

            coordinates = np.fromstring(key, np.float64, 2)

            for m in range(self._num_meshes):

                if counts[m] == 0:

                    centroid_trees[m].query()


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

def set_to_coordinate_array(s):

    arr = np.empty((len(s), 2), dtype=np.float64)

    for i, key in enumerate(s):

        arr[i] = np.fromstring(key, np.float64, 2)

    return arr

def barycentric(points, triangles):
    """Compute barycentric coordinates

    n = number of points to calculate coordinates for
    points = ndarray (n, 2)
    triangles = ndarray (n, 3, 2)
    """


    u = triangles[:,1,:] - triangles[:,0,:]
    v = triangles[:,2,:] - triangles[:,0,:]
    w = points - triangles[:,0,:]

    uv = np.cross(u, v)
    uw = np.cross(u, w)
    vw = np.cross(v, w)

    b = np.empty((points.shape[0], 3), dtype=np.float64)
    b[:,1] = vw / -uv
    b[:,2] = uw / uv
    b[:,0] = 1.0 - b[:,1] - b[:,2]

    return b, np.bitwise_and.reduce(np.greater_equal(b, 0), axis=1)

