from Adcirc.Files import Fort63


filename = '/home/tristan/Development/adcirc-comparisons/Data/black/fort.63'
f = Fort63(filename)
f.load()
print(f.data().shape)