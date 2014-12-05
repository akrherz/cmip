'''
Copy the Hayhoe data into my local database

   model   | scenario 
-----------+----------
 echam5    | a1b x
 echo      | a1b x
 cnrm      | a1b x
 cgcm3_t47 | a1b x
 miroc_hi  | a1b x
 hadgem    | a1b x
 cgcm3_t63 | a1b x
 hadcm3    | a1b x
 pcm       | a1b x
 giss_aom  | a1b x

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

tmdata = pr_nc.variables['time'][:]
print basets, np.shape(tmdata)[0] / 365.0

# Files have degrees east 0-360, so 190 is -170 , 200 is -160
lons = pr_nc.variables['lon'][:] - 360.0
lats = pr_nc.variables['lat'][:]

def do(lon, lat, station):

    idx = np.digitize([lon,], lons)[0]
    jdx = np.digitize([lat,], lats)[0]

    pdata = pr_nc.variables['pr'][:,jdx,idx]
    xdata = tasmax_nc.variables['tmax'][:,jdx,idx]
    ndata = tasmin_nc.variables['tmin'][:,jdx,idx]

    highs = temperature(xdata, 'C').value('F')
    lows = temperature(ndata, 'C').value('F')
    precips = pdata / 24.5

    now = basets
    for k, val in enumerate(tmdata):
        now += datetime.timedelta(days=1)
        if now.month == 2 and now.day == 29:
            # Insert missing data
            cursor.execute("""
        INSERT into hayhoe_daily(model, scenario, station, day, high, low,
        precip) values (%s, %s, %s, %s, %s, %s, %s)
        """, (model, scenario, station, now, high, low, precip))            
            now += datetime.timedelta(days=1)
        high = float(highs[k])
        low = float(lows[k])
        if low > high:
            # Swap, sigh
            print '%s %s high: %.1f low: %.1f was swapped' % (
                        now.strftime("%m-%d-%Y"), station, high, low)
            high2 = high
            high = low
            low = high2
        precip = float(precips[k])
        cursor.execute("""
        INSERT into hayhoe_daily(model, scenario, station, day, high, low,
        precip) values (%s, %s, %s, %s, %s, %s, %s)
        """, (model, scenario, station, now, high, low, precip))
            

for line in open('cscap_sites.csv'):
    lon, lat, station = line.strip().split(",")
    print 'Processing %s' % (station,)
    do(float(lon), float(lat), station)
    
cursor.close()
PGCONN.commit()
PGCONN.close()