import netCDF4
import datetime
import numpy as np
from pyiem.plot import MapPlot
import util

hussnc = netCDF4.Dataset('../cnrm_cm3/sresa1b/huss_A1_2000_2299.nc')
nc = netCDF4.Dataset('../cnrm_cm3/sresa1b/ps_A1.nc')
lats = nc.variables['lat'][:]
lons = nc.variables['lon'][:] 

idx1 = util.find_time_idx(nc, datetime.datetime(2046,1,1) )
idx2 = util.find_time_idx(nc, datetime.datetime(2064,12,1) ) + 1

data = np.average(nc.variables['ps'][idx1+5:idx2+1:12,:,:], 0)
hussdata = np.average(hussnc.variables['huss'][idx1+5:idx2+1:12,:,:], 0)

r = hussdata / (1 - hussdata)
e = r * data / (0.622 + r)
e = np.where(e < 0.00000001, 0.00000001, e)
td = (243.5 * np.log10(e) - 440.8) / (19.48 - np.log10(e))
#td = np.log10(e)

m = MapPlot(sector='conus')
lons, lats = np.meshgrid(lons, lats)
#m.pcolormesh(lons, lats, td, np.linspace(np.min(td), np.max(td), 12),
m.pcolormesh(lons, lats, td, np.linspace(0,30, 12),
            clip_on=False )
m.postprocess(filename='test.png')