from Utilities.Printable import Printable
from scipy.io import netcdf as nc

class GeoWriter(Printable):

    def __init__(self, file, coordinates):

        super().__init__('NetCDF Writer')

        self._f = nc.netcdf_file(file, 'w', version=2)

        self._f.createDimension('lon', coordinates.shape[0])
        self._f.createDimension('lat', coordinates.shape[0])
        self._f.createDimension('bnds', 2)

        f_lon = self._f.createVariable('lon', coordinates.dtype, ('lon',))
        f_lat = self._f.createVariable('lat', coordinates.dtype, ('lat',))

        f_lon.units = 'degrees_east'
        f_lat.units = 'degrees_north'

        f_lon[:] = coordinates[:,0]
        f_lat[:] = coordinates[:,1]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        # Write the file
        self._f.close()

    def write_variable(self, name, variable, fill_value=-99999):

        var = self._f.createVariable(name, variable.dtype, ('lon',))
        var[:] = variable[:]