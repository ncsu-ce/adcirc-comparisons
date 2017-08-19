import numpy as np

# Point = np.dtype({
#     'names': ['x', 'y'],
#     'formats': [np.float64, np.float64]
# })

Point = np.dtype([('coords', np.float64, (2,))])

Element = np.dtype({
    'names': ['n1', 'n2', 'n3'],
    'formats': [np.uint32, np.uint32, np.uint32]
})

# ElementCoordinates = np.dtype({
#     'names': ['x1', 'y1', 'x2', 'y2', 'x3', 'y3'],
#     'formats': [np.float64, np.float64, np.float64, np.float64, np.float64, np.float64]
# })

ElementCoordinates = np.dtype([('coords', np.float64, (6,))])