from DataStructures.Datatypes import Point, Element, ElementCoordinates
import numpy as np

a = np.empty(3, dtype=Point)
a[0] = 0, 1
a[1] = 1, 1
a[2] = 5, 6
print(a)

b = np.empty(1, dtype=ElementCoordinates)
b[0] = [a[0], a[1], a[2]]
print(b)
