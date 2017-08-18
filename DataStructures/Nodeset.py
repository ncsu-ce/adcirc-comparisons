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

        # Get all nodal coordinates
        nodal_coordinates = self._meshes[_mesh_index].node_coordinates()

        # mask out values not in the bounding box
        in_range = np.all(
            np.logical_and(
                self._ll <= nodal_coordinates,
                self._ur >= nodal_coordinates
            ), axis=1
        )

        return nodal_coordinates, in_range

    def _find_all_nodes(self):

        self.message('Finding common nodes')
        self._common_nodes = set()
        self._uncommon_nodes = [set()]*self._num_meshes
        appears = defaultdict(lambda: array('b', [0] * self._num_meshes))

        for m in range(self._num_meshes):

            nodal_coordinates, in_range = self._coordinates_in_range(m)

            # If the node appears, flip the mesh index to true
            for n in range(nodal_coordinates.shape[0]):

                if in_range[n]:

                    appears[nodal_coordinates[n].tobytes()][m] = 1

        # FIGURE THIS OUT YA IDIOT
        # for key, counts in appears.items():
        #
        #     for m in range(self._num_meshes):
        #
        #         if counts[m] == self._num_meshes:
        #
        #             self._common_nodes.add(key)

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
