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

pr_nc = netCDF4.Dataset(("data/" "%s.a1b.pr.NAm.grid.1960.2099.nc") % (MODEL,))
tasmin_nc = netCDF4.Dataset(
    ("data/" "%s.a1b.tmin.NAm.grid.1960.2099.nc") % (MODEL,)
)
tasmax_nc = netCDF4.Dataset(
    ("data/" "%s.a1b.tmax.NAm.grid.1960.2099.nc") % (MODEL,)
)

lons = pr_nc.variables["lon"][:]
lats = pr_nc.variables["lat"][:]

# The calendar is 365 day, so we have some concerns to deal with
t0idx = (2046 - 1960) * 365
t1idx = (2066 - 1960) * 365

t0 = datetime.datetime(2044, 1, 1)
t1 = datetime.datetime(2066, 1, 1)

for i, lon in enumerate(lons):
    print "%s/%s" % (i, len(lons))
    for j, lat in enumerate(lats):
        if lon < 262 or lon > 283 or lat < 34 or lat > 48:
            continue
        precip = pr_nc.variables["pr"][t0idx:t1idx, j, i]
        tasmax = tasmax_nc.variables["tmax"][t0idx:t1idx, j, i]
        tasmin = tasmin_nc.variables["tmin"][t0idx:t1idx, j, i]

        pfn = "%s/%.4f_%.4f.pcp" % (outdir, lon - 360.0, lat)
        tfn = "%s/%.4f_%.4f.tmp" % (outdir, lon - 360.0, lat)
        pfp = open(pfn, "w")
        tfp = open(tfn, "w")
        pfp.write(
            """BCCA Lon: %s Lat: %s



"""
            % (lon, lat)
        )
        tfp.write(
            """BCCA Lon: %s Lat: %s



"""
            % (lon, lat)
        )
        now = t0
        k = 0
        while now < t1:
            if now.month == 2 and now.day == 29:
                pfp.write(
                    "%s%03i%5.1f\n"
                    % (now.year, float(now.strftime("%j")), -99)
                )
                tfp.write(
                    "%s%03i%5.1f%5.1f\n"
                    % (now.year, float(now.strftime("%j")), -99, -99)
                )
                now += datetime.timedelta(days=1)
            pfp.write(
                "%s%03i%5.1f\n"
                % (now.year, float(now.strftime("%j")), precip[k])
            )
            tmax = tasmax[k]
            tmin = tasmin[k]
            if tmax < tmin:
                tmp = tmin
                tmin = tmax
                tmax = tmp
            tfp.write(
                "%s%03i%5.1f%5.1f\n"
                % (now.year, float(now.strftime("%j")), tmax, tmin)
            )
            k += 1
            now += datetime.timedelta(days=1)
        pfp.close()
        tfp.close()
