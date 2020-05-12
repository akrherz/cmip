import matplotlib.pyplot as plt
import netCDF4
import datetime
import numpy
import network
import psycopg2
import matplotlib.pyplot as plt

COOP = psycopg2.connect(database="coop", host="iemdb", user="nobody")
cursor = COOP.cursor()

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

pr_nc = netCDF4.Dataset(
    "bcca3/miroc3_2_medres.1.sresa1b.c20c3m.1981_2000.pr.nc"
)
lats = pr_nc.variables["lat"][:]
lons = pr_nc.variables["lon"][:]

stid = "IA0200"
j = numpy.digitize([nt.sts[stid]["lat"]], lats)
i = numpy.digitize([nt.sts[stid]["lon"]], lons)
precip = pr_nc.variables["pr"][0, :, j, i] / 25.4

obs = []
cursor.execute(
    """SELECT precip from alldata_ia WHERE 
    station = %s and year > 1980 and year < 2000""",
    (stid,),
)
for row in cursor:
    obs.append(row[0])

obs = numpy.array(obs)

(fig, ax) = plt.subplots(1, 1)

bins = [0, 0.05, 0.1, 0.25, 0.5, 1, 10000]
ovals = []
mvals = []
for i in range(len(bins) - 1):
    ovals.append(
        numpy.sum(
            numpy.where(
                numpy.logical_and(obs >= bins[i], obs < bins[i + 1]), obs, 0
            )
        )
        / 19.0
    )
    mvals.append(
        numpy.sum(
            numpy.where(
                numpy.logical_and(precip >= bins[i], precip < bins[i + 1]),
                precip,
                0,
            )
        )
        / 19.0
    )

ax.bar(
    numpy.arange(0, 6) - 0.3,
    ovals,
    label='Obs   %.2f"' % (sum(ovals),),
    facecolor="r",
    width=0.3,
)
ax.bar(
    numpy.arange(0, 6),
    mvals,
    label='BCCA3 %.2f"' % (sum(mvals),),
    facecolor="b",
    width=0.3,
)

ax.legend(loc="best")
ax.set_xticks(range(0, 6))
ax.set_xticklabels(
    ("0-0.05", "0.05-0.1", "0.1-0.25", "0.25-0.5", "0.5-1.0", "1.0+")
)
ax.set_title("1981-1999 Ames, IA Precipitation Totals by bin")
ax.set_ylabel("Yearly Precipitation [inch]")
ax.set_xlabel("Daily Precipitation Bin [inch]")
ax.grid(True)

fig.savefig("test.png")
