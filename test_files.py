from testing_files import *
from Adcirc.Files import Fort14

files = Desktop()
fort14 = Fort14(files.qa)

nodes = fort14.node_coordinates()
ele_coords = fort14.element_coordinates()
centroids = fort14.centroids()
bounds = fort14.bounds()

# print(nodes.shape)
# print(ele_coords.shape)
# print(centroids.shape)
# print(bounds)
print(fort14.element_coordinates(0))