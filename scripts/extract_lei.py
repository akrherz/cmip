import psycopg2
from pyiem.network import Table as NetworkTable

pgconn = psycopg2.connect(database="coop")
cursor = pgconn.cursor()
nt = NetworkTable("CSCAP")

models = ["cgcm3_t63", "hadgem", "echo", "cnrm", "pcm"]

for sid in ["GILMORE", "ISUAG", "SEPAC", "BRADFORD.A"]:
    climatesite = nt.sts[sid]["climate_site"]
    for model in models:
        outfn = "data/%s_%s_%s.txt" % (sid, model, "a1b")
        o = open(outfn, "w")
        o.write("year,month,avg_temp_c,precip_mm\n")
        cursor.execute(
            """SELECT extract(year from day) as yr,
        extract(month from day) as mo, avg((f2c(high)+f2c(low))/2.0),
        sum(precip) * 25.4 from hayhoe_daily where model = %s
        and scenario = 'a1b' and station = %s and day >= '2005-01-01'
        GROUP by yr, mo ORDER by yr, mo""",
            (model, climatesite),
        )
        for row in cursor:
            if row[3] is None or row[2] is None:
                continue
            o.write("%.0f,%.0f,%.2f,%.2f\n" % row)
        o.close()
