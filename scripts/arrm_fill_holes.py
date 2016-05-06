"""
 The sampled ARRM data for the CSCAP sites has one day holes due to various
 lame reasons.  Lets see if we can fill those in...

 + echam5 had a number of missing days for high in Sept 2070 for IA, IL, WI
 + echo had no data for 31 Dec 2099
 + cnrm had just a few dates with missing low temperatures
 + cgcm3_t47 is missing an entire year
 + miroc_hi is missing a number of years
 + hadgem had no data for 31 Dec 2099
 + cgcm3_t63 is missing an entire year
"""
import psycopg2.extras
from pyiem.network import Table as NetworkTable
import sys
import datetime
pgconn = psycopg2.connect(database='coop')
cursor = pgconn.cursor()
cursor2 = pgconn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cursor3 = pgconn.cursor()

MODEL = sys.argv[1]
SCENARIO = sys.argv[2]

nt = NetworkTable("CSCAP")

done = []
# for sid in nt.sts.keys():
for sid in ['BDNM2',]:
    # sid = nt.sts[sid]['climate_site']
    if sid in done:
        continue
    done.append(sid)
    for varname in ['high', 'low', 'precip']:
        cursor2.execute("""
            WITH obs as (
            SELECT model, scenario, station, day,
            """+varname+""",
            lag("""+varname+""") OVER (ORDER by day ASC) as la,
            lead("""+varname+""") OVER (ORDER by day ASC) as le
            from hayhoe_daily WHERE model = %s
            and scenario = %s and station =%s
            )

            SELECT * from obs where """+varname+""" is null and
            la is not null and le is not null
            """, (MODEL, SCENARIO, sid))
        for row2 in cursor2:
            if varname == 'precip':
                newval = "%.2f" % ((row2['la'] + row2['le'])/2.)
            else:
                newval = int((row2['la'] + row2['le'])/2.)
            cursor3.execute("""UPDATE hayhoe_daily SET """+varname+""" = %s
                WHERE model = %s and scenario = %s and station = %s
                and day = %s""", (newval,
                                  MODEL, SCENARIO, sid, row2['day']))
        if cursor2.rowcount > 0:
            print "SID: %s varname: %-7s count: %-4s" % (sid, varname,
                                                         cursor2.rowcount)
    # Now lets check to see how much is left
    cursor.execute("""SELECT day, high, low, precip from hayhoe_daily where
    model = %s and scenario = %s and station = %s and
    (high is null or low is null or precip is null)""", (MODEL, SCENARIO, sid))
    cnt = cursor.rowcount
    if cnt > 0:
        print("----> %s rows with nulls for %s" % (cnt, sid))
        if cnt < 20:
            for row in cursor:
                newhigh = row[1]
                newlow = row[2]
                newprecip = row[3]
                if row[1] is None:
                    cursor2.execute("""SELECT avg(high) from hayhoe_daily where
                    model = %s and scenario = %s and day = %s and
                    high is not null""", (MODEL, SCENARIO, row[0]))
                    newhigh = cursor2.fetchone()[0]
                    if newhigh is None:
                        print 'Double Failure for high on %s' % (row[0],)
                        cursor2.execute("""SELECT avg(high) from hayhoe_daily where
                        model = %s and scenario = %s and day = %s and
                        high is not null
                        """, (MODEL, SCENARIO,
                              row[0] - datetime.timedelta(days=1)))
                        newhigh = cursor2.fetchone()[0]
                        if newhigh is None:
                            print 'Triple Failure for high on %s' % (row[0],)
                            continue
                if row[2] is None:
                    cursor2.execute("""SELECT avg(low) from hayhoe_daily where
                    model = %s and scenario = %s and day = %s and
                    low is not null""", (MODEL, SCENARIO, row[0]))
                    newlow = cursor2.fetchone()[0]
                    if newlow is None:
                        print 'Double Failure for low on %s' % (row[0],)
                        cursor2.execute("""
                        SELECT avg(low) from hayhoe_daily where
                        model = %s and scenario = %s and day = %s and
                        low is not null
                        """, (MODEL, SCENARIO,
                              row[0] - datetime.timedelta(days=1)))
                        newlow = cursor2.fetchone()[0]
                        if newlow is None:
                            print 'Triple Failure for low on %s' % (row[0],)
                            continue
                if row[3] is None:
                    cursor2.execute("""
                    SELECT avg(precip) from hayhoe_daily where
                    model = %s and scenario = %s and day = %s and
                    precip is not null""", (MODEL, SCENARIO, row[0]))
                    newprecip = cursor2.fetchone()[0]
                    if newprecip is None:
                        print 'Double Failure for precip on %s' % (row[0],)
                        cursor2.execute("""
                        SELECT avg(precip) from hayhoe_daily where
                        model = %s and scenario = %s and day = %s and
                        precip is not null
                        """, (MODEL, SCENARIO,
                              row[0] - datetime.timedelta(days=1)))
                        newprecip = cursor2.fetchone()[0]
                        if newprecip is None:
                            print 'Triple Failure for precip on %s' % (row[0],)
                            continue

                print(("%s %10s %10s %10s --> %5.1f %5.1f %5.2f"
                       ) % (row[0], row[1], row[2], row[3], newhigh,
                            newlow, newprecip))
                if newhigh < newlow:
                    newlow2 = newhigh
                    newhigh = newlow
                    newlow = newlow2
                cursor2.execute("""UPDATE hayhoe_daily SET high = %s, low = %s,
                precip = %s WHERE model = %s and scenario = %s and day = %s
                and station = %s""", (newhigh, newlow, newprecip, MODEL,
                                      SCENARIO, row[0], sid))

cursor3.close()
pgconn.commit()
