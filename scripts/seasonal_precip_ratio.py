"""
BCSD
"""

import netCDF4
from mpl_toolkits.basemap import Basemap
import datetime
import numpy
import numpy.ma
from pyiem.plot import MapPlot
import matplotlib.pyplot as plt

basets = datetime.datetime(1950,1,1)
days1 = (datetime.datetime(1981,1,1) - basets).days
days2 = (datetime.datetime(2000,1,1) - basets).days
days3 = (datetime.datetime(2046,1,1) - basets).days
days4 = (datetime.datetime(2065,1,1) - basets).days

#obs_nc = netCDF4.Dataset('1_8obs/obs_.125deg.monthly.OBS.Prcp.1950-1999.nc')
obs_nc = netCDF4.Dataset('bcsd3/sresa1b.miroc3_2_medres.1.monthly.Prcp.1950-2099.nc')
fut_nc = netCDF4.Dataset('bcsd3/sresa1b.miroc3_2_medres.1.monthly.Prcp.1950-2099.nc')
lats = fut_nc.variables['latitude'][:]
lons = fut_nc.variables['longitude'][:] 
x, y = numpy.meshgrid(lons, lats)

offset1, offset2 = numpy.digitize([days1,days2], obs_nc.variables['time'][:])
offset3, offset4 = numpy.digitize([days3,days4], fut_nc.variables['time'][:])
print offset1, offset2, offset2 - offset1
print offset3, offset4, offset4 - offset3

jan = numpy.average(obs_nc.variables['Prcp'][offset1+0:offset2:12,:,:],0)
feb = numpy.average(obs_nc.variables['Prcp'][offset1+1:offset2:12,:,:],0)
dec = numpy.average(obs_nc.variables['Prcp'][offset1+11:offset2:12,:,:],0)
obs = (jan + feb + dec)/3.0

jan = numpy.average(obs_nc.variables['Prcp'][offset3+0:offset4:12,:,:],0)
feb = numpy.average(obs_nc.variables['Prcp'][offset3+1:offset4:12,:,:],0)
dec = numpy.average(obs_nc.variables['Prcp'][offset3+11:offset4:12,:,:],0)
fut = (jan + feb + dec)/3.0

ratio = numpy.ma.array(fut / obs)
ratio.mask = numpy.where(ratio == 1, True, False)
print numpy.min(ratio), numpy.max(ratio)
m = MapPlot(sector='conus', caption='', nologo=True,
            title=r'MIROC3.2 exp1 BCSD DJF Precipitation Ratio A1B / C20',
            subtitle='Period: Jan 2046 - Dec 2064 divided by Jan 1981- Dec 1999')

m.pcolormesh(x, y, ratio, numpy.arange(0,2.5,0.1), latlon=True, units='ratio')

m.postprocess(filename='djf_ratio_bcsd_miroc_only.png')


