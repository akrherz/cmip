"""
  Extract the ARRM data for SWAT
  cgcm3_t47
  cgcm3_t63
  miroc_3_2_hires
  miroc3_2_medres
"""
import netCDF4
import datetime
import sys
import os

MODEL = sys.argv[1]
outdir = "swatfiles_%s" % (MODEL,)
if not os.path.isdir(outdir):
    os.makedirs(outdir)

basets = datetime.datetime(1959, 12, 31)

pr_nc = netCDF4.Dataset(('/tera13/akrherz/hayhoe/'
        +'%s.a1b.pr.NAm.grid.1960.2099.nc') % (MODEL,))
tasmin_nc = netCDF4.Dataset(('/tera13/akrherz/hayhoe/'
        +'%s.a1b.tmin.NAm.grid.1960.2099.nc') % (MODEL,))
tasmax_nc = netCDF4.Dataset(('/tera13/akrherz/hayhoe/'
        +'%s.a1b.tmax.NAm.grid.1960.2099.nc') % (MODEL,))

lons = pr_nc.variables['lon'][:]
lats = pr_nc.variables['lat'][:]

t0 = basets + datetime.timedelta(days=float(pr_nc.variables['time'][0]))
t1 = basets + datetime.timedelta(days=float(pr_nc.variables['time'][-1]))
print t0, t1

t0 = datetime.datetime(2046,1,1)
t1 = datetime.datetime(2066,1,1)
t0idx = (t0 - basets).days
t1idx = (t1 - basets).days

for i, lon in enumerate(lons):
    print "%s/%s" % (i, len(lons))
    for j, lat in enumerate(lats):
        if lon < 262 or lon > 283 or lat < 34 or lat > 48:
            continue
        precip = pr_nc.variables['pr'][t0idx:t1idx,j,i]
        tasmax = tasmax_nc.variables['tmax'][t0idx:t1idx,j,i]
        tasmin = tasmin_nc.variables['tmin'][t0idx:t1idx,j,i]

        pfn = "%s/%.4f_%.4f.pcp" % (outdir, lon - 360., lat)
        tfn = "%s/%.4f_%.4f.tmp" % (outdir, lon - 360., lat)
        pfp = open(pfn, 'w')
        tfp = open(tfn, 'w')
        pfp.write("""BCCA Lon: %s Lat: %s 



""" % (lon, lat) )
        tfp.write("""BCCA Lon: %s Lat: %s 



""" % (lon, lat) )
        now = t0
        k = 0
        while now < t1:
            pfp.write("%s%03i%5.1f\n" % (now.year, float(now.strftime("%j")),
                precip[k]))
            tfp.write("%s%03i%5.1f%5.1f\n" % (now.year, 
                float(now.strftime("%j")), tasmax[k], tasmin[k]))
            k += 1
            now += datetime.timedelta(days=1)
        pfp.close()
        tfp.close()
