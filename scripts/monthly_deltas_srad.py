"""
 2046 thru 2065
 1981 thru 2000

rsds
  netcdf units: Wm^-2    multiply by 86,400 divide by 1,000,000
  swat file has: MJ / day
"""

import netCDF4
import datetime
import numpy
from scipy import interpolate

t0 = datetime.datetime(1850,1,1)

def find_time_idx(nc, needle):
    times = nc.variables['time'][:]
    for i, time in enumerate(times):
        ts = t0 + datetime.timedelta(days=time)
        if ts.year == needle.year and ts.month == needle.month:
            return i
    return None

nc_20c = netCDF4.Dataset('pcmdi.ipcc4.miroc3_2_medres.20c3m.run1.monthly.rsds_A1.nc')
nc_a1b = netCDF4.Dataset('pcmdi.ipcc4.miroc3_2_medres.sresa1b.run1.monthly.rsds_A1.nc')
lats = nc_20c.variables['lat'][:]
lons = nc_20c.variables['lon'][:]

idx1_20c = find_time_idx(nc_20c, datetime.datetime(1981,1,1) )
idx2_20c = find_time_idx(nc_20c, datetime.datetime(2000,12,1) ) + 1
idx1_a1b = find_time_idx(nc_a1b, datetime.datetime(2046,1,1) )
idx2_a1b = find_time_idx(nc_a1b, datetime.datetime(2065,12,1) ) + 1

rsds_20c = nc_20c.variables['rsds'][idx1_20c:idx2_20c,:,:]
rsds_a1b = nc_a1b.variables['rsds'][idx1_a1b:idx2_a1b,:,:]

jan = numpy.average(rsds_a1b[::12,:,:],0) - numpy.average(rsds_20c[::12,:,:],0)
feb = numpy.average(rsds_a1b[1::12,:,:],0) - numpy.average(rsds_20c[1::12,:,:],0)
mar = numpy.average(rsds_a1b[2::12,:,:],0) - numpy.average(rsds_20c[2::12,:,:],0)
apr = numpy.average(rsds_a1b[3::12,:,:],0) - numpy.average(rsds_20c[3::12,:,:],0)
may = numpy.average(rsds_a1b[4::12,:,:],0) - numpy.average(rsds_20c[4::12,:,:],0)
jun = numpy.average(rsds_a1b[5::12,:,:],0) - numpy.average(rsds_20c[5::12,:,:],0)
jul = numpy.average(rsds_a1b[6::12,:,:],0) - numpy.average(rsds_20c[6::12,:,:],0)
aug = numpy.average(rsds_a1b[7::12,:,:],0) - numpy.average(rsds_20c[7::12,:,:],0)
sep = numpy.average(rsds_a1b[8::12,:,:],0) - numpy.average(rsds_20c[8::12,:,:],0)
oct = numpy.average(rsds_a1b[9::12,:,:],0) - numpy.average(rsds_20c[9::12,:,:],0)
nov = numpy.average(rsds_a1b[10::12,:,:],0) - numpy.average(rsds_20c[10::12,:,:],0)
dec = numpy.average(rsds_a1b[11::12,:,:],0) - numpy.average(rsds_20c[11::12,:,:],0)

jan_T = interpolate.RectBivariateSpline(lats, lons, jan)
feb_T = interpolate.RectBivariateSpline(lats, lons, feb)
mar_T = interpolate.RectBivariateSpline(lats, lons, mar)
apr_T = interpolate.RectBivariateSpline(lats, lons, apr)
may_T = interpolate.RectBivariateSpline(lats, lons, may)
jun_T = interpolate.RectBivariateSpline(lats, lons, jun)
jul_T = interpolate.RectBivariateSpline(lats, lons, jul)
aug_T = interpolate.RectBivariateSpline(lats, lons, aug)
sep_T = interpolate.RectBivariateSpline(lats, lons, sep)
oct_T = interpolate.RectBivariateSpline(lats, lons, oct)
nov_T = interpolate.RectBivariateSpline(lats, lons, nov)
dec_T = interpolate.RectBivariateSpline(lats, lons, dec)



o = open('WG_SWAT2009_F_SRAD.csv', 'w')
for i, line in enumerate(open('WG_SWAT2009.csv')):
    if i == 0:
        o.write(line)
        continue
    tokens = line.split(',')
    lat = float( tokens[6] )
    lon = float( tokens[7] )
    old = tokens[-36:-24]
    if i % 235 == 0:
        print tokens[4]
        d = map(float, old)
        for j in range(12):
            print "%5.2f" % (d[j]),
        print
    old[0] = "%.2f" % (max(0, float(old[0]) + (jan_T(lat, lon) * 86400.0 / 1000000.0)))
    old[1] = "%.2f" % (max(0, float(old[1]) + (feb_T(lat, lon) * 86400.0 / 1000000.0)))
    old[2] = "%.2f" % (max(0, float(old[2]) + (mar_T(lat, lon) * 86400.0 / 1000000.0)))
    old[3] = "%.2f" % (max(0, float(old[3]) + (apr_T(lat, lon) * 86400.0 / 1000000.0)))
    old[4] = "%.2f" % (max(0, float(old[4]) + (may_T(lat, lon) * 86400.0 / 1000000.0)))
    old[5] = "%.2f" % (max(0, float(old[5]) + (jun_T(lat, lon) * 86400.0 / 1000000.0)))
    old[6] = "%.2f" % (max(0, float(old[6]) + (jul_T(lat, lon) * 86400.0 / 1000000.0)))
    old[7] = "%.2f" % (max(0, float(old[7]) + (aug_T(lat, lon) * 86400.0 / 1000000.0)))
    old[8] = "%.2f" % (max(0, float(old[8]) + (sep_T(lat, lon) * 86400.0 / 1000000.0)))
    old[9] = "%.2f" % (max(0, float(old[9]) + (oct_T(lat, lon) * 86400.0 / 1000000.0)))
    old[10] = "%.2f" % (max(0, float(old[10]) + (nov_T(lat, lon) * 86400.0 / 1000000.0)))
    old[11] = "%.2f" % (max(0, float(old[11]) + (dec_T(lat, lon) * 86400.0 / 1000000.0)))
    for j in range(12):
        tokens[-36+j] = old[j]
    if i % 235 == 0:
        d = map(float, old)
        for j in range(12):
            print "%5.2f" % (d[j]),
        print
    o.write(",".join(tokens))
o.close()
