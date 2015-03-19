"""
Copy the Hayhoe data into my local database

   model   | scenario
-----------+----------
 echam5    | a1b -done-
 echo      | a1b -done-
 cnrm      | a1b -done-
 cgcm3_t47 | a1b missing one year
 miroc_hi  | a1b missing a number of years
 hadgem    | a1b -done-
 cgcm3_t63 | a1b missing one year
 hadcm3    | a1b missing a number of years
 pcm       | a1b missing Nov, Dec 2099
 giss_aom  | a1b missing a number of years

"""
import netCDF4
import datetime
import numpy as np
import psycopg2
from pyiem.datatypes import temperature, distance
import sys
from pyiem.network import Table as NetworkTable

PGCONN = psycopg2.connect(database='coop')
cursor = PGCONN.cursor()

model = sys.argv[1]
scenario = sys.argv[2]

nt = NetworkTable("CSCAP")
done = []

BASE = "/tera13/akrherz/hayhoe"

pr_nc = netCDF4.Dataset(('%s/%s.%s.pr.NAm.grid.1960.2099.nc'
                         ) % (BASE, model, scenario))
tasmax_nc = netCDF4.Dataset(('%s/%s.%s.tmax.NAm.grid.1960.2099.nc'
                             ) % (BASE, model, scenario))
tasmin_nc = netCDF4.Dataset(('%s/%s.%s.tmin.NAm.grid.1960.2099.nc'
                             ) % (BASE, model, scenario))

tokens = (pr_nc.variables['time'].units).replace("days since ", "").split("-")
basets = datetime.date(int(tokens[0]), int(tokens[1]), int(tokens[2]))

tmdata = pr_nc.variables['time'][:]
if basets != datetime.date(1959, 12, 31):
    print('FAILURE, basets %s is not 31 Dec 1959' % (basets,))
    sys.exit()
if (np.shape(tmdata)[0] / 365.0) != 140:
    print(('FAILURE, %s years found, not exactly 140'
           ) % (np.shape(tmdata)[0] / 365.0,))
    sys.exit()

# Files have degrees east 0-360, so 190 is -170 , 200 is -160
lons = pr_nc.variables['lon'][:] - 360.0
lats = pr_nc.variables['lat'][:]


def fix(val):
    """ Convert a value into something reasonable """
    if np.ma.is_masked(val):
        return None
    return float(val)


def insert(station, now, high, low, precip):
    """ Add a database entry """
    cursor.execute("""
    INSERT into hayhoe_daily(model, scenario, station, day, high, low, precip)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (model, scenario, station, now, high, low, precip))


def do(lon, lat, station):
    """ Process this station and geography """
    idx = np.digitize([lon, ], lons)[0]
    jdx = np.digitize([lat, ], lats)[0]
    print("--> Processing %s i:%s j:%s" % (station, idx, jdx))

    pdata = pr_nc.variables['pr'][:, jdx, idx]
    xdata = tasmax_nc.variables['tmax'][:, jdx, idx]
    ndata = tasmin_nc.variables['tmin'][:, jdx, idx]

    highs = temperature(xdata, 'C').value('F')
    lows = temperature(ndata, 'C').value('F')
    precips = distance(pdata, 'MM').value('IN')

    now = basets
    high = low = precip = None
    for k, _ in enumerate(tmdata):
        now += datetime.timedelta(days=1)
        if now.month == 2 and now.day == 29:
            # Insert missing data
            insert(station, now, high, low, precip)
            now += datetime.timedelta(days=1)
        high = fix(highs[k])
        low = fix(lows[k])
        if low is not None and high is not None and low > high:
            # Swap, sigh
            print(('%s %s high: %.1f low: %.1f was swapped'
                   ) % (now.strftime("%m-%d-%Y"), station, high, low))
            high2 = high
            high = low
            low = high2
        precip = fix(precips[k])
        insert(station, now, high, low, precip)

do(-122.83, 38.40, 'BDCAL')
do(-87.87, 46.81, 'BDMIC')
# for sid in nt.sts.keys():
#    climatesite = nt.sts[sid]['climate_site']
#    if climatesite in done:
#        continue
#    done.append(climatesite)
#    do(nt.sts[sid]['lon'], nt.sts[sid]['lat'], climatesite)

cursor.close()
PGCONN.commit()
PGCONN.close()
