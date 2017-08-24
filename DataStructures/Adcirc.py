from Utilities.Printable import Printable
from Adcirc.Files import Fort14, Fort63, Fort64
from os.path import isfile

class AdcircRun(Printable):

    def __init__(self, directory):

        super().__init__('ADCIRC Run')

        d = directory.strip()
        if not d[-1] == '/':
            d += '/'

        if isfile(d + 'fort.14'):
            self.mesh = Fort14(d + 'fort.14')
        else:
            self.message('ERROR: No fort.14 file found')
            return

        if isfile(d + 'fort.63'):
            self.elevation_timeseries = Fort63(d + 'fort.63')
        else:
            self.elevation_timeseries = None

        if isfile(d + 'fort.64'):
            self.velocity_timeseries = Fort64(d + 'fort.64')
        else:
            self.elevation_timeseries = None