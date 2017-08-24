from Comparisons.Comparator import Comparator
from Comparisons.Comparisons import AverageDifference
from DataStructures.Adcirc import AdcircRun

# original = AdcircRun('/home/tristan/box/adcirc/runs/refinement/original')
refined1 = AdcircRun('/home/tristan/box/adcirc/runs/refinement/4')
refined2 = AdcircRun('/home/tristan/box/adcirc/runs/refinement/16')

compare = Comparator([])
nodes, errors = compare.compare_elevation_timeseries(refined1, [refined2])

print(nodes.shape)
print(errors.shape)

with open('results.txt', 'w') as f:

    f.write('x,y,error\n')

    for i in range(nodes.shape[0]):

        f.write('{},{},{}\n'.format(nodes[i,0], nodes[i,1], 'nan' if errors[i,0] == -99999.0 else errors[i,0]))