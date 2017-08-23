from Adcirc.Files import Fort63, Fort64
from Interpolators.Timeseries import TimeseriesInterpolator

f = Fort63('/home/tristan/Development/adcirc-comparisons/Data/black/fort.63')
f64 = Fort64('/home/tristan/Development/adcirc-comparisons/Data/black/fort.64')
f.load()
f64.load()
t = TimeseriesInterpolator(f)
t64 = TimeseriesInterpolator(f64)
d, mask = t64.timestep(4.8)


# print(d[0])
# print(mask[0])