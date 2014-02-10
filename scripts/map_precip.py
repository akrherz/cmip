"""
(1)  mean precip over the period 1981-1999 from the gridded 2 degree obs.
(2)  mean precip over the period 1981-1999 for the raw MIROC 3.2 output.
(3) mean precip over the period 1981-1999 for bias-corrected MIROC 3.2.

It would be interesting if you could also make difference plots for (2)
minus (1) and (3) minus (1), but don't put a lot of effort into that.

BCSD
"""

import netCDF4
from mpl_toolkits.basemap import Basemap
import datetime
import numpy
from pyiem.plot import MapPlot
import matplotlib.pyplot as plt

basets2 = datetime.datetime(1850,1,1)
days21 = (datetime.datetime(1981,1,1) - basets2).days
days22 = (datetime.datetime(2000,1,1) - basets2).days

basets = datetime.datetime(1950,1,1)
days1 = (datetime.datetime(1981,1,1) - basets).days
days2 = (datetime.datetime(2000,1,1) - basets).days

#miroc_nc = netCDF4.Dataset('miroc3_2_medres/pcmdi.ipcc4.miroc3_2_medres.20c3m.run1.monthly.pr_A1.nc')
bc3_nc = netCDF4.Dataset('bc3/Extraction_Prcp.nc')
#obs2_nc = netCDF4.Dataset('2obs/Extraction_Prcp.nc')
#pr_nc = netCDF4.Dataset('bcsd3/miroc3_2_medres.1.sresa1b.c20c3m.1981_2000.pr.nc')
#pr_nc2 = netCDF4.Dataset('bcca3/miroc3_2_medres.1.sresa1b.c20c3m.1981_2000.pr.nc')
#lats = pr_nc.variables['latitude'][:]
#lons = pr_nc.variables['longitude'][:] - 0.0
#lats = obs2_nc.variables['latitude'][:]
#lons = obs2_nc.variables['longitude'][:] - 0.0
#lats = miroc_nc.variables['lat'][:]
#lons = miroc_nc.variables['lon'][:] 
lats = bc3_nc.variables['latitude'][:]
lons = bc3_nc.variables['longitude'][:] 
print lons
#offset1, offset2 = numpy.digitize([days1,days2], pr_nc.variables['time'][:]) 
#offset1, offset2 = numpy.digitize([days1,days2], obs2_nc.variables['time'][:]) 
offset1, offset2 = numpy.digitize([days1,days2], bc3_nc.variables['time'][:]) 
print offset1, offset2
#offset3, offset4 = numpy.digitize([days1,days2], pr_nc2.variables['time'][:]) 
#offset3, offset4 = numpy.digitize([days1,days2], miroc_nc.variables['time'][:]) 
#print offset3, offset4

#pr = numpy.average(pr_nc.variables['Prcp'][0,offset1:offset2,:,:] ,0)
#pr = numpy.average(obs2_nc.variables['Prcp'][0,offset1:offset2,:,:] ,0)
#pr = numpy.average(miroc_nc.variables['pr'][offset3:offset4,:,:] ,0)
#pr2 = numpy.average(pr_nc2.variables['pr'][0,offset3:offset4,:,:] ,0)
pr = numpy.average(bc3_nc.variables['Prcp'][0,offset1:offset2,:,:] ,0)



m = MapPlot(sector='conus', caption='', nologo=True,
            title=r'1981-1999 MIROC3.2 Bias Correction 3 (bc3)',
            subtitle='Yearly Average Precipitation')

#            urcrnrlon=-78,urcrnrlat=49, projection='merc',                       
#                lat_0=45.,lon_0=-92.,lat_ts=42.,
#                           resolution='i', fix_aspect=False)
x, y = numpy.meshgrid(lons, lats)
#colormap = LevelColormap([1,6,12,18,24,30,36,42,48,54,60,66,72,78,84], plt.cm.gist_ncar)

levels = [1,6,12,18,24,30,36,42,48,54,60,66,72,78,84]
#levels = numpy.arange(-14,14,2)
m.pcolormesh(x, y, pr  * 365.0 / 25.4, levels, latlon=True, units='inches')
#m.drawstates()
#m.drawcoastlines()
#ax.set_title(r"1981-1999 MIROC 3.2 downscaled BCCA [inch/yr]")

#fig.colorbar(cs)

#fig.savefig('test.png')

m.postprocess(filename='test.png')


