from Adcirc.Files import Fort14
from Utilities.Printable import Printable
from collections import defaultdict, Counter
import numpy as np
import time

Printable.print_header()

qa = '/home/tristan/box/adcirc/domains/qa/fort.14'
full = '/home/tristan/box/adcirc/domains/full/fort.14'
louisiana = '/home/tristan/box/adcirc/domains/louisiana/fort.14'
black = '/home/tristan/box/research/adcirc/python/Data/black/fort.14'
blue = '/home/tristan/box/research/adcirc/python/Data/blue/fort.14'
red = '/home/tristan/box/research/adcirc/python/Data/red/fort.14'

f = Fort14(full)

s = time.time()
centroids = f.centroids()
f = time.time()

print('Centroids shape:', centroids.shape)
print('Generate centroids:', f-s, 'seconds')

def test_hashing(centroids_array):
    asint = centroids_array.view(np.int64)
    # bits = np.bitwise_or(np.left_shift(asint[:,0], 32), asint[:,1])
    bits = np.bitwise_xor(asint[:,0], asint[:,1])

    _s = time.time()
    _c = Counter()
    for i in range(bits.shape[0]):
        # print(centroids[i], bits[i])
        _c[bits[i]] += 1
    _f = time.time()

    print(_c.most_common(1))
    print('Build dictionary using hash:', _f-_s, 'seconds')

def test_bytes(centroids_array):
    _s = time.time()
    _c = Counter()
    for i in range(centroids_array.shape[0]):
        _c[centroids[i].tobytes()] += 1
    _f = time.time()

    print(_c.most_common(1))
    print('Build dictionary using bytes:', _f-_s, 'seconds')

test_hashing(centroids)
test_bytes(centroids)