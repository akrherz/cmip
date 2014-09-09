'''
  Convert the downscaled Hayhoe data into something SWAT wants/likes
'''
import netCDF4
import datetime
import numpy as np
import psycopg2
from pyiem.datatypes import temperature
import sys

PGCONN = psycopg2.connect(database='coop')
cursor = PGCONN.cursor()

model = sys.argv[1]
scenario = sys.argv[2]

pr_nc = netCDF4.Dataset('/tera13/akrherz/hayhoe/%s.%s.pr.NAm.grid.1960.2099.nc' % (model, scenario))
tasmax_nc = netCDF4.Dataset('/tera13/akrherz/hayhoe/%s.%s.tmax.NAm.grid.1960.2099.nc' % (model, scenario))
tasmin_nc = netCDF4.Dataset('/tera13/akrherz/hayhoe/%s.%s.tmin.NAm.grid.1960.2099.nc' % (model, scenario))

tokens = (pr_nc.variables['time'].units).replace("days since ", "").split("-")
basets = datetime.datetime( int(tokens[0]), int(tokens[1]), int(tokens[2]) )

# Files have degrees east 0-360, so 190 is -170 , 200 is -160
lons = pr_nc.variables['lon'][:] - 360.0
lats = pr_nc.variables['lat'][:]

t0 = datetime.datetime(2001,1,1)
t1 = datetime.datetime(2099,1,1)
t0idx = int((t0 - basets).days)
t1idx = int((t1 - basets).days)

def do(lon, lat, station):

    idx = np.digitize([lon,], lons)[0]
    jdx = np.digitize([lat,], lats)[0]

    pdata = pr_nc.variables['pr'][t0idx:t1idx,jdx,idx]
    xdata = tasmax_nc.variables['tmax'][t0idx:t1idx,jdx,idx]
    ndata = tasmin_nc.variables['tmin'][t0idx:t1idx,jdx,idx]

    highs = temperature(xdata, 'C').value('F')
    lows = temperature(ndata, 'C').value('F')
    precips = pdata / 24.5


    now = t0
    k = 0
    while now < t1:
        high = float(highs[k])
        low = float(lows[k])
        precip = float(precips[k])
        #print now, high, low, precip
        #if highs.mask[k]:
        #    high = None
        #if lows.mask[k]:
        #    low = None
        #if precips.mask[k]:
        #    precip = None
        cursor.execute("""
        INSERT into hayhoe_daily(model, scenario, station, day, high, low,
        precip) values (%s, %s, %s, %s, %s, %s, %s)
        """, (model, scenario, station, now, high, low, precip))
        k += 1
        now += datetime.timedelta(days=1)

for line in open('cscap_sites.csv'):
    lon, lat, station = line.strip().split(",")
    do(float(lon), float(lat), station)
    
cursor.close()
PGCONN.commit()
PGCONN.close()