from Adcirc.Files import Fort14
from DataStructures.Nodeset import Nodeset

qa = '/home/tristan/box/adcirc/domains/qa/fort.14'
scaled = '/home/tristan/box/adcirc/runs/scaled20-refinement/original/fort.14'
full = '/home/tristan/box/adcirc/domains/full/fort.14'
louisiana = '/home/tristan/box/adcirc/domains/louisiana/fort.14'
black = '/home/tristan/box/research/adcirc/python/Data/black/fort.14'
blue = '/home/tristan/box/research/adcirc/python/Data/blue/fort.14'
red = '/home/tristan/box/research/adcirc/python/Data/red/fort.14'

# f1 = Fort14(scaled)
# f2 = Fort14(full)
# n = Nodeset([f1, f2])

f1 = Fort14(red)
f2 = Fort14(blue)
f3 = Fort14(black)
n = Nodeset([f1, f2, f3])

# f1 = Fort14(louisiana)
# f2 = Fort14(full)
# n = Nodeset([f1, f2])
