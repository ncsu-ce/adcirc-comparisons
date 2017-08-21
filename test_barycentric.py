import numpy as np
from DataStructures.Nodeset import barycentric

points = np.empty((2, 2), dtype=np.float64)
triangles = np.empty((2, 3, 2), dtype=np.float64)

points[0] = 2, 2
points[1] = 2, 2
triangles[0] = [[1, 1], [3, 1], [2, 4]]
triangles[1] = [[3, 1], [2, 4], [4, 4]]

bary, mask = barycentric(points, triangles)

print(bary)
print(mask)