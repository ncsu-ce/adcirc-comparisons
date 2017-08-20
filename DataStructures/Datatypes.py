import numpy as np

Point = np.dtype({
    'names': ['x', 'y'],
    'formats': [np.float64, np.float64]
})

# Element = np.dtype({
#     'names': ['n1', 'n2', 'n3'],
#     'formats': [np.uint32, np.uint32, np.uint32]
# })
#
# ElementCoordinates = np.dtype({
#     'names': ['n1', 'n2', 'n3'],
#     'formats': [Point, Point, Point]
# })