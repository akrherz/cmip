"""
Plot the Yearly Average Precipitation
"""
import netCDF4
import glob
import os
import sys
import datetime
import numpy as np
from pyiem.plot import MapPlot
import matplotlib.cm as cm

t1981 = datetime.datetime(2046, 1, 1)
t1999 = datetime.datetime(2064, 12, 31)


def get_time(nc):
    """ Get the time indexes """
    tm = nc.variables["time"]
    tokens = tm.units.split()
    sts = datetime.datetime.strptime(tokens[2], "%Y-%m-%d")
    lookup = (t1981 - sts).days
    idx0 = np.digitize([lookup], tm[:])[0]
    lookup = (t1999 - sts).days
    idx1 = np.digitize([lookup], tm[:])[0]
    return idx0, idx1


def run(fn):
    """ Run for a given filename! """
    nc = netCDF4.Dataset(fn, "r")
    # time
    idx0, idx1 = get_time(nc)

    # somewhat a hack for now
    dmul = 1.0
    if (idx1 - idx0) == 19:
        dmul = 1.0
    elif (idx1 - idx0) / 19.0 < 13:
        dmul = 365.0 / 12.0
    # Either pr or Prcp
    pvar = "pr" if nc.variables.has_key("pr") else "Prcp"
    pmul = 1.0 if nc.variables[pvar].units in ["mm/d", "mm"] else 86400.0
    precip = (
        np.sum(nc.variables[pvar][idx0 : idx1 + 1, :, :], 0)
        * dmul
        * pmul
        / 19.0
        / 24.5
    )
    # lat or latitude
    latvar = "lat" if nc.variables.has_key("lat") else "latitude"
    lats = nc.variables[latvar][:]
    lats = np.concatenate([lats, [lats[-1] + (lats[-1] - lats[-2])]])
    # lon or longitude
    lonvar = "lon" if nc.variables.has_key("lon") else "longitude"
    lons = nc.variables[lonvar][:] - 360.0
    lons = np.concatenate([lons, [lons[-1] + (lons[-1] - lons[-2])]])
    print fn, np.shape(lons), np.shape(lats), np.max(precip)
    try:
        title = "2046-2065 Precip %s" % (nc.title,)
    except:
        title = "2046-2065 Yearly Average Precipitation "
    subtitle = "filename: %s" % (fn,)
    m = MapPlot(
        title=title, subtitle=subtitle, sector="conus", nologo=True, caption=""
    )
    x, y = np.meshgrid(lons, lats)
    cmap = cm.get_cmap("gist_rainbow")
    cmap.set_over("black")
    m.pcolormesh(
        x,
        y,
        precip,
        np.array([0, 1, 5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 100]),
        cmap=cmap,
        units="inch/yr",
    )

    m.postprocess(filename="/tmp/plots/%s.png" % (fn.replace(".nc", ""),))
    nc.close()

    m.close()


if __name__ == "__main__":
    os.chdir("/tera13/akrherz/hayhoe/yearly")
    for fn in glob.glob("*pr.NAm*.nc"):
        run(fn)
        # sys.exit()
