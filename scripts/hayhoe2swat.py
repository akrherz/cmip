'''
  Convert the downscaled Hayhoe data into something SWAT wants/likes
'''
import netCDF4
import datetime
import numpy as np

pr_nc = netCDF4.Dataset('/tera13/akrherz/hayhoe/hadcm3.a1b.pr.NAm.grid.1960.2099.nc')
tasmax_nc = netCDF4.Dataset('/tera13/akrherz/hayhoe/hadcm3.a1b.tmax.NAm.grid.1960.2099.nc')
tasmin_nc = netCDF4.Dataset('/tera13/akrherz/hayhoe/hadcm3.a1b.tmin.NAm.grid.1960.2099.nc')

tokens = (pr_nc.variables['time'].units).replace("days since ", "").split("-")
basets = datetime.datetime( int(tokens[0]), int(tokens[1]), int(tokens[2]) )

# Files have degrees east 0-360, so 190 is -170 , 200 is -160
lons = pr_nc.variables['lon'][:] - 360.0
lats = pr_nc.variables['lat'][:]

t0 = datetime.datetime(2046,1,1)
t1 = datetime.datetime(2065,1,1)
t0idx = int((t0 - basets).days)
t1idx = int((t1 - basets).days)

for i, lon in enumerate(lons):
    print "%s/%s" % (i, len(lons))
    for j, lat in enumerate(lats):
        if lon < -104.2 or lon > -80.1:
            continue
        if lat < 35.4 or lat > 49.5:
            continue
        precip = pr_nc.variables['pr'][:,j,i]
        tasmax = tasmax_nc.variables['tmax'][:,j,i] 
        print tasmax, np.max(tasmax)
        tasmin = tasmin_nc.variables['tmin'][:,j,i] 

        pfn = "swatfiles/%.4f_%.4f.pcp" % (0 - lon, lat)
        tfn = "swatfiles/%.4f_%.4f.tmp" % (0 - lon, lat)
        pfp = open(pfn, 'w')
        tfp = open(tfn, 'w')
        pfp.write("""BCCA Lon: %s Lat: %s 



""" % (lon, lat) )
        tfp.write("""BCCA Lon: %s Lat: %s 



""" % (lon, lat) )
        now = t0
        k = t0idx
        while now <= t1:
            pfp.write("%s%03i%5.1f\n" % (now.year, float(now.strftime("%j")),
                precip[k]))
            tfp.write("%s%03i%5.1f%5.1f\n" % (now.year, 
                float(now.strftime("%j")), tasmax[k], tasmin[k]))
            k += 1
            now += datetime.timedelta(days=1)
        pfp.close()
        tfp.close()
