"""
 The sampled ARRM data for the CSCAP sites has one day holes due to various
 lame reasons.  Lets see if we can fill those in...
"""
import psycopg2.extras
from pyiem.network import Table as NetworkTable
import sys
pgconn = psycopg2.connect(database='coop')
cursor = pgconn.cursor()
cursor2 = pgconn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cursor3 = pgconn.cursor()

MODEL = sys.argv[1]
SCENARIO = sys.argv[2]

nt = NetworkTable("CSCAP")

done = []
for sid in nt.sts.keys():
    sid = nt.sts[sid]['climate_site']
    if sid in done:
        continue
    done.append(sid)
    cursor2.execute("""
        WITH obs as (
        SELECT model, scenario, station, day, high, low, precip,
        lag(high) OVER (ORDER by day ASC) as lag_high,
        lag(low) OVER (ORDER by day ASC) as lag_low,
        lag(precip) OVER (ORDER by day ASC) as lag_precip,
        lead(high) OVER (ORDER by day ASC) as lead_high,
        lead(low) OVER (ORDER by day ASC) as lead_low,
        lead(precip) OVER (ORDER by day ASC) as lead_precip
        from hayhoe_daily WHERE model = %s and scenario = %s and station =%s
        )
        
        SELECT * from obs where high is null 
        and lag_high is not null and
        lead_high is not null and lag_low is not null and
        lead_low is not null
        """, (MODEL, SCENARIO, sid))
    for row2 in cursor2:
        cursor3.execute("""UPDATE hayhoe_daily SET high = %s, low = %s,
            precip = %s WHERE model = %s and scenario = %s and station = %s
            and day = %s""", (int((row2['lag_high'] + row2['lead_high'])/2.) ,
            int((row2['lag_low'] + row2['lead_low'])/2.) ,
            "%.2f" % ((row2['lag_precip'] + row2['lead_precip'])/2.,),
            MODEL, SCENARIO, sid, row2['day']))
    print sid, cursor2.rowcount
    
cursor3.close()
pgconn.commit()