"""
We have MIROC3_2_MEDRES
  -
"""

import matplotlib.pyplot as plt
import netCDF4
import datetime
import numpy
import network
import psycopg2

nt = network.Table(
    (
        "IACLIMATE",
        "MNCLIMATE",
        "NDCLIMATE",
        "SDCLIMATE",
        "NECLIMATE",
        "KSCLIMATE",
        "MOCLIMATE",
        "KYCLIMATE",
        "ILCLIMATE",
        "WICLIMATE",
        "INCLIMATE",
        "OHCLIMATE",
        "MICLIMATE",
    )
)

pr_nc = netCDF4.Dataset("2obs/Extraction_Prcp.nc")
pr_nc2 = netCDF4.Dataset("bc3/Extraction_Prcp.nc")
mon_pr_nc = netCDF4.Dataset(
    "miroc3_2_medres/pcmdi.ipcc4.miroc3_2_medres.20c3m.run1.monthly.pr_A1.nc"
)
lats = pr_nc.variables["latitude"][:]
lons = pr_nc.variables["longitude"][:] - 0.0
mon_lats = mon_pr_nc.variables["lat"][:]
mon_lons = mon_pr_nc.variables["lon"][:] - 0.0
tm = pr_nc.variables["time"][:]
mon_tm = mon_pr_nc.variables["time"][:]

stid = "IA0200"
j = numpy.digitize([nt.sts[stid]["lat"]], lats)
i = numpy.digitize([nt.sts[stid]["lon"]], lons)
mon_j = numpy.digitize([nt.sts[stid]["lat"]], mon_lats)
mon_i = numpy.digitize([nt.sts[stid]["lon"] + 360.0], mon_lons)

basets = datetime.datetime(1950, 1, 1)
mon_basets = datetime.datetime(1850, 1, 1)

data = []
data2 = []
data3 = []
for yr in range(1981, 2000):
    days1 = (datetime.datetime(yr, 1, 1) - basets).days
    days2 = (datetime.datetime(yr + 1, 1, 1) - basets).days
    idx1 = numpy.digitize([days1], tm)
    idx2 = numpy.digitize([days2], tm)
    data.append(
        numpy.sum(pr_nc.variables["Prcp"][0, idx1:idx2, j, i]) / 25.4 * 30.4
    )
    data2.append(
        numpy.sum(pr_nc2.variables["Prcp"][0, idx1:idx2, j, i]) / 25.4 * 30.4
    )

    days1 = (datetime.datetime(yr, 1, 1) - mon_basets).days
    days2 = (datetime.datetime(yr + 1, 1, 1) - mon_basets).days
    idx1 = numpy.digitize([days1], mon_tm)
    idx2 = numpy.digitize([days2], mon_tm)
    data3.append(
        numpy.sum(mon_pr_nc.variables["pr"][idx1:idx2, mon_j, mon_i])
        / 25.4
        * 86400.0
        * 31.0
    )

(fig, ax) = plt.subplots(1, 1)

ax.bar(
    numpy.arange(1981, 2000) - 0.45,
    data3,
    fc="g",
    ec="g",
    width=0.3,
    label="MIROC3_2 $2^\circ$ PCMDI",
)
ax.bar(
    numpy.arange(1981, 2000) - 0.15,
    data,
    fc="r",
    ec="r",
    width=0.3,
    label=r"Gridded $2^\circ$ Obs",
)
ax.bar(
    numpy.arange(1981, 2000) + 0.15,
    data2,
    fc="b",
    ec="b",
    width=0.3,
    label="MIROC3_2 Bias Correct",
)
ax.plot([1981, 2000], [32, 32])
ax.text(1981, 32.4, "1950-2010 Climatology")
ax.set_xlim(1980.5, 2000.5)
ax.legend(ncol=2, fontsize=12)
ax.set_ylim(0, 65)
ax.grid(True)
ax.set_ylabel("Yearly Precipitation [inch]")
ax.set_title("MIROC3.2 MEDRES Yearly Precip for Ames, IA")

fig.savefig("test.png")
