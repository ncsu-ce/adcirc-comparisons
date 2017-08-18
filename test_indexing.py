from Adcirc.Files import Fort14
from collections import defaultdict
import numpy as np
import time
import sys

# f = '/home/tristan/box/adcirc/domains/qa/fort.14'
# f = '/home/tristan/box/adcirc/domains/full/fort.14'
# f = '/home/tristan/box/adcirc/domains/louisiana/fort.14'

f1 = '/home/tristan/box/research/adcirc/python/Data/black/fort.14'
f2 = '/home/tristan/box/research/adcirc/python/Data/blue/fort.14'
f3 = '/home/tristan/box/research/adcirc/python/Data/red/fort.14'

m1 = Fort14(f1)
m2 = Fort14(f2)
m3 = Fort14(f3)

e1 = m1.element_coordinates()
e2 = m2.element_coordinates()
e3 = m3.element_coordinates()

e = [e1, e2, e3, e1]
d = defaultdict(lambda: [-1]*len(e))

for j in range(len(e)):

    coordinates = e[j]
    num_elements = coordinates.shape[0]

    for i in range(num_elements):

        element = coordinates[i]
        key_values = element[np.lexsort((element[:,1], element[:,0]))]
        key = tuple(key_values.flatten())

        d[key][j] = i
        # print(sys.getsizeof(key), key)

    # print(coordinates.shape)

for key, values in d.items():
    print(key, values)

a = (1,)
b = (1, 2)
c = tuple()
print(a, sys.getsizeof(a))
print(b, sys.getsizeof(b))
print(c, sys.getsizeof(c))
# mask = np.lexsort((e3[:,:,1], e3[:,:,0]))
#
# print(e3)
# print(mask)