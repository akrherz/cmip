import matplotlib.pyplot as plt
import netCDF4
import datetime
import numpy
import network
import psycopg2
from mpl_toolkits.basemap import Basemap

pr_nc = netCDF4.Dataset('f/bcca3/bcca3_0/Extraction_pr.nc')
#pr_nc = netCDF4.Dataset('ob/1_8obs/Extraction_pr.nc')
lats = pr_nc.variables['lat'][:]
lons = pr_nc.variables['lon'][:] - 0.0

pr = pr_nc.variables['pr'][0,:,:,:]
avgpr = numpy.average(numpy.where(pr < 1000, pr, 0), 0)

import matplotlib.pyplot as plt

(fig, ax) = plt.subplots(1,1)

m = Basemap(llcrnrlon=-110,llcrnrlat=31,
            urcrnrlon=-78,urcrnrlat=49, projection='merc',                       
		lat_0=45.,lon_0=-92.,lat_ts=42.,
                           resolution='i', fix_aspect=False)
x, y = numpy.meshgrid(lons, lats)
cs = m.contourf(x,y,avgpr * 365.0 / 25.4,cmap=plt.cm.gist_ncar, latlon=True,
    levels=[1,6,12,18,24,30,36,42,48,54,60,66,72,78,84])
m.drawstates()
ax.set_title("CMIP3 MIROC3_2 BCCA Downscaled 1/8 degree\n2046-2065 Precipitation [inch/yr]")

fig.colorbar(cs)

fig.savefig('test.png')
