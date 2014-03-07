"""
 2046 thru 2065
 1981 thru 2000

3.  The moisture variable will be the biggest problem.  The variable we have
available is near-surface specific humidity (CMIP3 variable name "huss") and
we need to get from there to a delta for dew point.  The procedure is a
little complicated.  For each monthly data record, do the following:

(i)  First compute mixing ratio (r) from specific humidity (q) using the
formula r = q / (1 - q)

(ii)  Then compute vapor pressure (e) from r and surface pressure (p) using
the formula e = r*p / (x+r) where x = 0.622.  Surface pressure is CMIP3
variable name "ps".  Convert e from Pascals to millibars in the usual way
(simply divide by 100).

(iii)  Compute composite annual cycles of e for the current and future
climate simulations.

(iv)  For each month in the composite annual cycles, compute dew point (Td)
using the formula:
Td = (243.5 ln(e) - 440.8) / (19.48 - ln(e) )
Here e is in millibars and Td is in Celsius.  Reference for this formula is
Bolton (1980), Monthly Weather Review.

(v)  For each month in the composite annual cycles, subtract Td for current
climate from Td for future climate to get the delta.  Then add this to the
observed annual cycle of Td.


"""

import netCDF4
import datetime
import numpy
from scipy import interpolate
import util


nc_20c_ps = netCDF4.Dataset('../hadcm3/20c3m/ps_A1.nc')
nc_20c_huss = netCDF4.Dataset('../hadcm3/20c3m/huss_A1.nc')
nc_a1b_ps = netCDF4.Dataset('../hadcm3/sresa1b/ps_A1.nc')
nc_a1b_huss = netCDF4.Dataset('../hadcm3/sresa1b/huss_A1.nc')

lats = nc_20c_ps.variables['lat'][:]
lons = nc_20c_ps.variables['lon'][:]

print 'HADCM3 HACK HERE!'
idx1_20c = util.find_time_idx(nc_20c_ps, datetime.datetime(1981,1,1) )
idx2_20c = util.find_time_idx(nc_20c_ps, datetime.datetime(1999,12,1) ) + 1
idx1_a1b = util.find_time_idx(nc_a1b_ps, datetime.datetime(2046,1,1) )
idx2_a1b = util.find_time_idx(nc_a1b_ps, datetime.datetime(2064,12,1) ) + 1

ps_20c = nc_20c_ps.variables['ps'][idx1_20c:idx2_20c,:,:] / 100.0
huss_20c = nc_20c_huss.variables['huss'][idx1_20c:idx2_20c,:,:]
r_20c = huss_20c / (1 - huss_20c)
e_20c = r_20c * ps_20c / (0.622 + r_20c)

ps_a1b = nc_a1b_ps.variables['ps'][idx1_20c:idx2_20c,:,:] / 100.0
huss_a1b = nc_a1b_huss.variables['huss'][idx1_20c:idx2_20c,:,:]
r_a1b = huss_a1b / (1 - huss_a1b)
e_a1b = r_a1b * ps_a1b / (0.622 + r_a1b)

a1b_jan = numpy.average(e_a1b[::12,:,:],0)
a1b_feb = numpy.average(e_a1b[1::12,:,:],0)
a1b_mar = numpy.average(e_a1b[2::12,:,:],0)
a1b_apr = numpy.average(e_a1b[3::12,:,:],0)
a1b_may = numpy.average(e_a1b[4::12,:,:],0)
a1b_jun = numpy.average(e_a1b[5::12,:,:],0)
a1b_jul = numpy.average(e_a1b[6::12,:,:],0)
a1b_aug = numpy.average(e_a1b[7::12,:,:],0)
a1b_sep = numpy.average(e_a1b[8::12,:,:],0)
a1b_oct = numpy.average(e_a1b[9::12,:,:],0)
a1b_nov = numpy.average(e_a1b[10::12,:,:],0)
a1b_dec = numpy.average(e_a1b[11::12,:,:],0)

c20_jan = numpy.average(e_20c[::12,:,:],0)
c20_feb = numpy.average(e_20c[1::12,:,:],0)
c20_mar = numpy.average(e_20c[2::12,:,:],0)
c20_apr = numpy.average(e_20c[3::12,:,:],0)
c20_may = numpy.average(e_20c[4::12,:,:],0)
c20_jun = numpy.average(e_20c[5::12,:,:],0)
c20_jul = numpy.average(e_20c[6::12,:,:],0)
c20_aug = numpy.average(e_20c[7::12,:,:],0)
c20_sep = numpy.average(e_20c[8::12,:,:],0)
c20_oct = numpy.average(e_20c[9::12,:,:],0)
c20_nov = numpy.average(e_20c[10::12,:,:],0)
c20_dec = numpy.average(e_20c[11::12,:,:],0)

a1b_jan_td = (243.5 * numpy.log10(a1b_jan) - 440.8) / (19.48 - numpy.log10(a1b_jan))
a1b_feb_td = (243.5 * numpy.log10(a1b_feb) - 440.8) / (19.48 - numpy.log10(a1b_feb))
a1b_mar_td = (243.5 * numpy.log10(a1b_mar) - 440.8) / (19.48 - numpy.log10(a1b_mar))
a1b_apr_td = (243.5 * numpy.log10(a1b_apr) - 440.8) / (19.48 - numpy.log10(a1b_apr))
a1b_may_td = (243.5 * numpy.log10(a1b_may) - 440.8) / (19.48 - numpy.log10(a1b_may))
a1b_jun_td = (243.5 * numpy.log10(a1b_jun) - 440.8) / (19.48 - numpy.log10(a1b_jun))
a1b_jul_td = (243.5 * numpy.log10(a1b_jul) - 440.8) / (19.48 - numpy.log10(a1b_jul))
a1b_aug_td = (243.5 * numpy.log10(a1b_aug) - 440.8) / (19.48 - numpy.log10(a1b_aug))
a1b_sep_td = (243.5 * numpy.log10(a1b_sep) - 440.8) / (19.48 - numpy.log10(a1b_sep))
a1b_oct_td = (243.5 * numpy.log10(a1b_oct) - 440.8) / (19.48 - numpy.log10(a1b_oct))
a1b_nov_td = (243.5 * numpy.log10(a1b_nov) - 440.8) / (19.48 - numpy.log10(a1b_nov))
a1b_dec_td = (243.5 * numpy.log10(a1b_dec) - 440.8) / (19.48 - numpy.log10(a1b_dec))

c20_jan_td = (243.5 * numpy.log10(c20_jan) - 440.8) / (19.48 - numpy.log10(c20_jan))
c20_feb_td = (243.5 * numpy.log10(c20_feb) - 440.8) / (19.48 - numpy.log10(c20_feb))
c20_mar_td = (243.5 * numpy.log10(c20_mar) - 440.8) / (19.48 - numpy.log10(c20_mar))
c20_apr_td = (243.5 * numpy.log10(c20_apr) - 440.8) / (19.48 - numpy.log10(c20_apr))
c20_may_td = (243.5 * numpy.log10(c20_may) - 440.8) / (19.48 - numpy.log10(c20_may))
c20_jun_td = (243.5 * numpy.log10(c20_jun) - 440.8) / (19.48 - numpy.log10(c20_jun))
c20_jul_td = (243.5 * numpy.log10(c20_jul) - 440.8) / (19.48 - numpy.log10(c20_jul))
c20_aug_td = (243.5 * numpy.log10(c20_aug) - 440.8) / (19.48 - numpy.log10(c20_aug))
c20_sep_td = (243.5 * numpy.log10(c20_sep) - 440.8) / (19.48 - numpy.log10(c20_sep))
c20_oct_td = (243.5 * numpy.log10(c20_oct) - 440.8) / (19.48 - numpy.log10(c20_oct))
c20_nov_td = (243.5 * numpy.log10(c20_nov) - 440.8) / (19.48 - numpy.log10(c20_nov))
c20_dec_td = (243.5 * numpy.log10(c20_dec) - 440.8) / (19.48 - numpy.log10(c20_dec))

jan = a1b_jan_td - c20_jan_td
feb = a1b_feb_td - c20_feb_td
mar = a1b_mar_td - c20_mar_td
apr = a1b_apr_td - c20_apr_td
may = a1b_may_td - c20_may_td
jun = a1b_jun_td - c20_jun_td
jul = a1b_jul_td - c20_jul_td
aug = a1b_aug_td - c20_aug_td
sep = a1b_sep_td - c20_sep_td
october = a1b_oct_td - c20_oct_td
nov = a1b_nov_td - c20_nov_td
dec = a1b_dec_td - c20_dec_td

jan_T = interpolate.RectBivariateSpline(lats, lons, jan)
feb_T = interpolate.RectBivariateSpline(lats, lons, feb)
mar_T = interpolate.RectBivariateSpline(lats, lons, mar)
apr_T = interpolate.RectBivariateSpline(lats, lons, apr)
may_T = interpolate.RectBivariateSpline(lats, lons, may)
jun_T = interpolate.RectBivariateSpline(lats, lons, jun)
jul_T = interpolate.RectBivariateSpline(lats, lons, jul)
aug_T = interpolate.RectBivariateSpline(lats, lons, aug)
sep_T = interpolate.RectBivariateSpline(lats, lons, sep)
oct_T = interpolate.RectBivariateSpline(lats, lons, october)
nov_T = interpolate.RectBivariateSpline(lats, lons, nov)
dec_T = interpolate.RectBivariateSpline(lats, lons, dec)



o = open('../hadcm3/WG_SWAT2009_F_SRAD_WND_DEW.csv', 'w')
for i, line in enumerate(open('../hadcm3/WG_SWAT2009_F_SRAD_WND.csv')):
    if i == 0:
        o.write(line)
        continue
    tokens = line.split(',')
    lat = float( tokens[6] )
    lon = float( tokens[7] )
    old = tokens[-24:-12]
    if i % 235 == 0:
        print tokens[4]
        d = map(float, old)
        for j in range(12):
            print "%5.2f" % (d[j]),
        print
    old[0] = "%.2f" % ( float(old[0]) + (jan_T(lat, lon) ))
    old[1] = "%.2f" % ( float(old[1]) + (feb_T(lat, lon) ))
    old[2] = "%.2f" % ( float(old[2]) + (mar_T(lat, lon) ))
    old[3] = "%.2f" % ( float(old[3]) + (apr_T(lat, lon) ))
    old[4] = "%.2f" % ( float(old[4]) + (may_T(lat, lon) ))
    old[5] = "%.2f" % ( float(old[5]) + (jun_T(lat, lon) ))
    old[6] = "%.2f" % ( float(old[6]) + (jul_T(lat, lon) ))
    old[7] = "%.2f" % ( float(old[7]) + (aug_T(lat, lon) ))
    old[8] = "%.2f" % ( float(old[8]) + (sep_T(lat, lon) ))
    old[9] = "%.2f" % ( float(old[9]) + (oct_T(lat, lon) ))
    old[10] = "%.2f" % ( float(old[10]) + (nov_T(lat, lon) ))
    old[11] = "%.2f" % ( float(old[11]) + (dec_T(lat, lon) ))
    for j in range(12):
        tokens[-24+j] = old[j]
    if i % 235 == 0:
        d = map(float, old)
        for j in range(12):
            print "%5.2f" % (d[j]),
        print
    o.write(",".join(tokens))
o.close()
