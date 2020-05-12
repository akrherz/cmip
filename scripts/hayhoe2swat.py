"""
  Convert the downscaled Hayhoe data into something SWAT wants/likes
"""
import netCDF4
import datetime
import numpy as np

pr_nc = netCDF4.Dataset(
    "/tera13/akrherz/hayhoe/miroc_hi.a1b.pr.NAm.grid.1960.2099.nc"
)
tasmax_nc = netCDF4.Dataset(
    "/tera13/akrherz/hayhoe/miroc_hi.a1b.tmax.NAm.grid.1960.2099.nc"
)
tasmin_nc = netCDF4.Dataset(
    "/tera13/akrherz/hayhoe/miroc_hi.a1b.tmin.NAm.grid.1960.2099.nc"
)

tokens = (pr_nc.variables["time"].units).replace("days since ", "").split("-")
basets = datetime.datetime(int(tokens[0]), int(tokens[1]), int(tokens[2]))

# Files have degrees east 0-360, so 190 is -170 , 200 is -160
lons = pr_nc.variables["lon"][:] - 360.0
lats = pr_nc.variables["lat"][:]

t0 = datetime.datetime(2046, 1, 1)
t1 = datetime.datetime(2065, 1, 1)
t0idx = int((t0 - basets).days)
t1idx = int((t1 - basets).days)

idx1 = np.digitize([-80.1], lons)[0]
idx0 = np.digitize([-104.2], lons)[0]
jdx0 = np.digitize([35.4], lats)[0]
jdx1 = np.digitize([49.5], lats)[0]


pdata = pr_nc.variables["pr"][t0idx:t1idx, jdx0:jdx1, idx0:idx1]

xdata = tasmax_nc.variables["tmax"][t0idx:t1idx, jdx0:jdx1, idx0:idx1]

ndata = tasmin_nc.variables["tmin"][t0idx:t1idx, jdx0:jdx1, idx0:idx1]


for j in range(jdx0, jdx1):
    lat = lats[j]

    for i in range(idx0, idx1):
        lon = lons[i]
        if lon < -104.2 or lon > -80.1:
            continue
        if lat < 35.4 or lat > 49.5:
            continue

        pfn = "swatfiles/%.4f_%.4f.pcp" % (0 - lon, lat)
        tfn = "swatfiles/%.4f_%.4f.tmp" % (0 - lon, lat)
        pfp = open(pfn, "w")
        tfp = open(tfn, "w")
        pfp.write(
            """Hayhoe Lon: %s Lat: %s 



"""
            % (lon, lat)
        )
        tfp.write(
            """Hayhoe Lon: %s Lat: %s 



"""
            % (lon, lat)
        )
        now = t0
        k = 0
        while now < t1:
            pfp.write(
                "%s%03i%5.1f\n"
                % (
                    now.year,
                    float(now.strftime("%j")),
                    pdata[k, j - jdx0, i - idx0],
                )
            )
            tfp.write(
                "%s%03i%5.1f%5.1f\n"
                % (
                    now.year,
                    float(now.strftime("%j")),
                    xdata[k, j - jdx0, i - idx0],
                    ndata[k, j - jdx0, i - idx0],
                )
            )
            k += 1
            now += datetime.timedelta(days=1)
        pfp.close()
        tfp.close()
