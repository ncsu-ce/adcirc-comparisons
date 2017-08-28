from Comparisons.Comparator import Comparator
from DataStructures.Adcirc import AdcircRun
import sys

def compare(baseline, other, outdir):

    c = Comparator([])
    nodes, errors, maximums = c.compare_elevation_timeseries(AdcircRun(baseline), [AdcircRun(other)])

    with open(outdir + '/average_error.csv', 'w') as f:

        f.write('x,y,error\n')

        for i in range(nodes.shape[0]):

            f.write('{},{},{}\n'.format(nodes[i, 0], nodes[i, 1], 'nan' if errors[i, 0] == -99999.0 else errors[i, 0]))

    with open(outdir + '/maximum_error.csv', 'w') as f:

        f.write('x,y,error\n')

        for i in range(nodes.shape[0]):

            f.write('{},{},{}\n'.format(nodes[i, 0], nodes[i, 1], 'nan' if errors[i, 0] == -99999.0 else maximums[i, 0]))

if __name__ == '__main__':

    if len(sys.argv) == 4:

        run1 = sys.argv[1]
        run2 = sys.argv[2]
        out = sys.argv[3]

        compare(run1, run2, out)

    else:

        print('Usage: python3 average_error.py [ADCIRC Run Directory] [ADCIRC Run Directory] [Output directory]')