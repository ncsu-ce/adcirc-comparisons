from Utilities.Printable import Printable
from scipy.io import netcdf as nc
from scipy.interpolate import griddata
import numpy as np

class GriddedGeoWriter(Printable):

    def __init__(self, file, coordinates, resolution):

        super().__init__('NetCDF Writer')

        self._f = nc.netcdf_file(file, 'w', version=2)
        self._coordinates = coordinates

        # Create the grid
        mins = np.amin(coordinates, axis=0)
        maxs = np.amax(coordinates, axis=0)
        self._grid_x, self._grid_y = np.mgrid[mins[0]:maxs[0]:resolution*1j, mins[1]:maxs[1]:resolution*1j]

        self._f.createDimension('lon', resolution)
        self._f.createDimension('lat', resolution)

        f_lon = self._f.createVariable('lon', self._grid_x.dtype, ('lon',))
        f_lat = self._f.createVariable('lat', self._grid_y.dtype, ('lat',))

        f_lon.units = 'degrees_east'
        f_lat.units = 'degrees_north'

        f_lon[:] = self._grid_x[:,0]
        f_lat[:] = self._grid_y[0,:]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._f.close()

    def write_variable(self, name, variable, fill_value=-99999):

        var = self._f.createVariable(name, variable.dtype, ('lon', 'lat'))

        data = griddata(self._coordinates, variable, (self._grid_x, self._grid_y), method='linear', fill_value=fill_value)
        var[:] = data[:]
        var._FillValue = fill_value


class GeoWriter(Printable):

    def __init__(self, file, coordinates):

        super().__init__('NetCDF Writer')

        self._f = nc.netcdf_file(file, 'w', version=2)

        self._f.createDimension('num_nodes', coordinates.shape[0])
        self._f.createDimension('bounds', 2)

        f_lon = self._f.createVariable('lon', coordinates.dtype, ('num_nodes',))
        f_lat = self._f.createVariable('lat', coordinates.dtype, ('num_nodes',))
        lon_bounds = self._f.createVariable('lon_bounds', coordinates.dtype, ('bounds',))
        lat_bounds = self._f.createVariable('lat_bounds', coordinates.dtype, ('bounds',))

        f_lon.units = 'degrees_east'
        f_lat.units = 'degrees_north'
        lon_bounds.units = 'degrees_east'
        lat_bounds.units = 'degrees_north'

        f_lon[:] = coordinates[:,0]
        f_lat[:] = coordinates[:,1]

        min_coords = np.amin(coordinates, axis=0)
        max_coords = np.amax(coordinates, axis=0)
        lon_bounds[:] = [min_coords[0], max_coords[0]]
        lat_bounds[:] = [min_coords[1], max_coords[1]]


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        # Write the file
        self._f.close()

    def write_variable(self, name, variable, fill_value=-99999):

        var = self._f.createVariable(name, variable.dtype, ('num_nodes',))
        var[:] = variable[:]
        var._FillValue = fill_value