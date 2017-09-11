from Adcirc.FilesNC import Fort63NC


with Fort63NC('/home/tristan/box/adcirc/runs/netcdf/fran/fort.63.nc') as f:

    # f.print_variables()
    f.print_everything()
    f.print_variables()