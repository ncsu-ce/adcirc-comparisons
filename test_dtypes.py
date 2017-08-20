from DataStructures.Datatypes import Point
import numpy as np

a = np.empty(3, dtype=Point)
a[0] = 0, 1
a[1] = 1, 1
a[2] = 5, 6
print(a)

b = np.empty((3, 2), dtype=np.float64)
b[0] = 0, 1
b[1] = 1, 1
b[2] = 5, 6
print(b)

c = b.view(Point)
print(c)
print(c.view(np.float64))
print(a.shape)
print(b.shape)
print(c.shape)