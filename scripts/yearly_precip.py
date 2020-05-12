import matplotlib.pyplot as plt
import netCDF4
import datetime
import numpy
import network
import psycopg2

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

pr_nc = netCDF4.Dataset("f/bcca5/Extraction_pr.nc")
# pr_nc = netCDF4.Dataset('ob/1_8obs/Extraction_pr.nc')
lats = pr_nc.variables["latitude"][:]
lons = pr_nc.variables["longitude"][:]

for stid in nt.sts.keys():
    if stid[2:] != "C005":
        continue
    j = numpy.digitize([nt.sts[stid]["lat"]], lats)
    i = numpy.digitize([360 + nt.sts[stid]["lon"]], lons)
    precip = pr_nc.variables["pr"][0, :, j, i]

    p = numpy.average(precip)
    cursor.execute(
        """SELECT sum(precip) from climate WHERE 
    station = %s""",
        (stid,),
    )
    row = cursor.fetchone()
    print(
        "%s RCP6: %6.1fmm %.2fin OBS: %6.1fmm %.2fin Diff: %.1f%%"
        % (
            stid[:2],
            p * 365.0,
            p * 365.0 / 25.4,
            row[0] * 25.4,
            row[0],
            ((p * 365.0 / 25.4) - row[0]) / row[0] * 100.0,
        )
    )
