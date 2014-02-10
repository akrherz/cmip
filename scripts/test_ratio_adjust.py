import numpy
import psycopg2
import datetime
from calendar import monthrange

DBCONN = psycopg2.connect(database='coop', host='iemdb', user='nobody')
cursor = DBCONN.cursor()

monthly = numpy.abs( numpy.random.randn(12) )
monthly = monthly / numpy.max(monthly)
monthly = numpy.concatenate([[monthly[-1],], monthly, [monthly[0],]])
# Extra to support beginning
daily = numpy.zeros( (366) )
x = []
for i in range(366):
    ts = datetime.datetime(2012,1,1) + datetime.timedelta(days=i)
    if ts.day == 15:
        x.append( i + 1)
x = numpy.concatenate([[-15,], x, [366+15,]])

xnew = numpy.interp(range(1,366), x, monthly)


cursor.execute("""SELECT extract(doy from day), month, precip from alldata_ia 
  WHERE station = 'IA0200' and year = 2013""")

mtotal = 0
dtotal = 0
original = 0
for row in cursor:
  original += row[2]
  mtotal += row[2] * monthly[ row[1] ]
  dtotal += row[2] * xnew[ row[0] ]

print 'ORIG: %.2f  MONTHLY ABJ: %.2f DAILY ABJ: %.2f' % (original, mtotal,
     dtotal)

import matplotlib.pyplot as plt

(fig, ax) = plt.subplots(1,1)

ax.plot(range(1,366), xnew, '-x')
ax.plot( x, monthly, 'o')
ax.set_xticks( (1,32,60,91,121,152,182,213,244,274,305,335,365) )
ax.set_xticklabels( ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec') )
ax.grid(True)
ax.set_title("Monthly to Daily Interpolation")
ax.set_ylabel("Dummy Delta")
fig.savefig('test.png')
