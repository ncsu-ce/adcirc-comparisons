from Adcirc.FilesNC import Fort63NC
from NC.Nodeset import Nodeset
from NC.Comparator import Comparator
from NC.Data import Variable
from scipy.io import netcdf as nc

f63 = '/home/tristan/box/adcirc/runs/netcdf/fran/fort.63.nc'

# with Fort63NC('/home/tristan/box/adcirc/runs/netcdf/fran/fort.64.nc') as f:
#
#     # f.print_everything()
#     f.print_variables()
#     f.print_some('time')

with Comparator(f63, [f63]) as test:

    average_elevation_error = test.avg_difference('zeta')
    print(average_elevation_error)

# nodes, indices = test.common_nodes()
# print(nodes[0], indices[0])

# indices = [0, 0, 0, 5]
# t0 = [0.9, 1, 2, 3, 4, 5]
# t1 = [0.5, 1, 2, 4, 5, 6, 7]
# t2 = [0.1, 1.1, 2, 3, 5, 7, 8]
# times = [t0, t1, t2]
# i = first_common_timestep(times)
# print(i)
# i = next_common_timestep(times, i)
# print(i)
# i = next_common_timestep(times, i)
# print(i)

#
# f = nc.netcdf_file(f63, 'r')
# test = Variable(f.variables['zeta'], [0, 1, 2])
# for i in range(10):
#     print(test.timestep(0, 1)(i/10))
# test = None
# f.close()