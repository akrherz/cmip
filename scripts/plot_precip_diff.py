"""
Plot the Yearly Average Precipitation

"""
titles = [
    "CMIP3 CCCMA CGCM3_1.1",
    "CMIP3 GFDL CM2_0.1",
    "CMIP3 GFDL CM2_1.1",
    "CMIP3 MIROC3_2 MEDRES",
    "CMIP3 ECHAM5.1",
    "CMIP5 GFDL CM3",
    "CMIP5 MIROC5",
    "CMIP5 MPI ESM LR",
    "CMIP5 MPI ESM MR",
]
pairs = """../data/bcsd_cccma_cgcm3_1.1.sresa1b.monthly.Prcp.1981_2000.nc
../data/cccma_cgcm3_1.gregorian.20c3m.run1.pr.BCCA_0.125deg.1981_2000.nc

../data/bcsd_gfdl_cm2_0.1.sresa1b.monthly.Prcp.1981_2000.nc
../data/gfdl_cm2_0.gregorian.20c3m.run1.pr.BCCA_0.125deg.1981_2000.nc

../data/bcsd_gfdl_cm2_1.1.sresa1b.monthly.Prcp.1981_2000.nc
../data/gfdl_cm2_1.gregorian.20c3m.run1.pr.BCCA_0.125deg.1981_2000.nc

../data/bcsd_miroc3_2_medres.1.sresa1b.monthly.Prcp.1981_2000.nc
../data/miroc3_2_medres.gregorian.20c3m.run1.pr.BCCA_0.125deg.1981_2000.nc

../data/bcsd_mpi_echam5.1.sresa1b.monthly.Prcp.1981_2000.nc
../data/mpi_echam5.gregorian.20c3m.run1.pr.BCCA_0.125deg.1981_2000.nc

../data/BCSD_0.125deg_pr_Amon_GFDL-CM3_historical_r1i1p1_195001-200512.nc
../data/BCCA_0.125deg_pr_day_GFDL-CM3_historical_r1i1p1_1980_2005.nc

../data/BCSD_0.125deg_pr_Amon_MIROC5_historical_r1i1p1_195001-200512.nc
../data/BCCA_0.125deg_pr_day_MIROC5_historical_r1i1p1_1980_2005.nc

../data/BCSD_0.125deg_pr_Amon_MPI-ESM-LR_historical_r1i1p1_195001-200512.nc
../data/BCCA_0.125deg_pr_day_MPI-ESM-LR_historical_r1i1p1_1980_2005.nc

../data/BCSD_0.125deg_pr_Amon_MPI-ESM-MR_historical_r1i1p1_195001-200512.nc
../data/BCCA_0.125deg_pr_day_MPI-ESM-MR_historical_r1i1p1_1980_2005.nc"""

import netCDF4
import glob
import os
import datetime
import numpy as np
from pyiem.plot import MapPlot
import matplotlib.cm as cm

t1981 = datetime.datetime(1981, 1, 1)
t1999 = datetime.datetime(1999, 12, 31)


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


def run(bcsdfn, bccafn, title):
    """ Run for a given filename! """
    nc = netCDF4.Dataset(bcsdfn, "r")
    # time
    idx0, idx1 = get_time(nc)
    # somewhat a hack for now
    dmul = 1.0
    if (idx1 - idx0) / 19.0 < 13:
        dmul = 365.0 / 12.0
    # Either pr or Prcp
    pvar = "pr" if nc.variables.has_key("pr") else "Prcp"
    pmul = 1.0 if nc.variables[pvar].units == "mm/d" else 86400.0
    bcsdprecip = (
        np.sum(nc.variables[pvar][idx0 : idx1 + 1, :, :], 0)
        * dmul
        * pmul
        / 19.0
        / 24.5
    )

    nc2 = netCDF4.Dataset(bccafn, "r")
    # time
    idx0, idx1 = get_time(nc2)
    # somewhat a hack for now
    dmul = 1.0
    if (idx1 - idx0) / 19.0 < 13:
        dmul = 365.0 / 12.0
    # Either pr or Prcp
    pvar = "pr" if nc2.variables.has_key("pr") else "Prcp"
    pmul = 1.0 if nc2.variables[pvar].units == "mm/d" else 86400.0
    bccaprecip = (
        np.sum(nc2.variables[pvar][idx0 : idx1 + 1, :, :], 0)
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
    lons = nc.variables[lonvar][:]
    lons = np.concatenate([lons, [lons[-1] + (lons[-1] - lons[-2])]])

    print np.shape(lons), np.shape(lats), np.max(bccaprecip), np.max(
        bcsdprecip
    )

    title = "81-99 Precip BCCA over BCSD %s" % (title,)
    # subtitle = 'filename: %s' % (bccafn,)
    m = MapPlot(
        title=title, subtitle="", sector="conus", nologo=True, caption=""
    )
    x, y = np.meshgrid(lons, lats)
    cmap = cm.get_cmap("Spectral")
    cmap.set_over("black")
    m.pcolormesh(
        x,
        y,
        bccaprecip / bcsdprecip * 100.0,
        np.arange(0, 201, 20),
        cmap=cmap,
        units="percentage",
    )
    png = "../cplots/%s.png" % (title.replace(" ", "_").lower(),)
    print png
    m.postprocess(filename=png)
    nc.close()
    nc2.close()


if __name__ == "__main__":
    for i, pr in enumerate(pairs.split("\n\n")):
        (f1, f2) = pr.split("\n")
        run(f1, f2, titles[i])
        # sys.exit()
