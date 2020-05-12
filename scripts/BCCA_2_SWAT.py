import netCDF4
import datetime

basets = datetime.datetime(1950, 1, 1)

pr_nc = netCDF4.Dataset("c20/bcca3/bcca3_0/Extraction_pr.nc")
tasmin_nc = netCDF4.Dataset("c20/bcca3/bcca3_0/Extraction_tasmin.nc")
tasmax_nc = netCDF4.Dataset("c20/bcca3/bcca3_0/Extraction_tasmax.nc")

lons = pr_nc.variables["lon"][:]
lats = pr_nc.variables["lat"][:]

t0 = basets + datetime.timedelta(days=pr_nc.variables["time"][0])
t1 = basets + datetime.timedelta(days=pr_nc.variables["time"][-1])
print t0, t1
sys.exit()

for i, lon in enumerate(lons):
    print "%s/%s" % (i, len(lons))
    for j, lat in enumerate(lats):
        precip = pr_nc.variables["pr"][0, :, j, i]
        tasmax = tasmax_nc.variables["tasmax"][0, :, j, i]
        tasmin = tasmin_nc.variables["tasmin"][0, :, j, i]

        pfn = "swatfiles/%.4f_%.4f.pcp" % (0 - lon, lat)
        tfn = "swatfiles/%.4f_%.4f.tmp" % (0 - lon, lat)
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
        while now <= t1:
            pfp.write(
                "%s%03i%5.1f\n"
                % (now.year, float(now.strftime("%j")), precip[k])
            )
            tfp.write(
                "%s%03i%5.1f%5.1f\n"
                % (now.year, float(now.strftime("%j")), tasmax[k], tasmin[k])
            )
            k += 1
            now += datetime.timedelta(days=1)
        pfp.close()
        tfp.close()
