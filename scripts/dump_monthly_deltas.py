"""
 Dump out what the monthly deltas should be
"""
import netCDF4
import datetime
import numpy

model = 'cnrm_cm3.1'

obs_nc = netCDF4.Dataset('../bcsd3/sresa1b.%s.monthly.Tavg.1950-2099.nc' % (model,))
fut_nc = netCDF4.Dataset('../bcsd3/sresa1b.%s.monthly.Tavg.1950-2099.nc' % (model,))
p_obs_nc = netCDF4.Dataset('../bcsd3/sresa1b.%s.monthly.Prcp.1950-2099.nc' % (model,))
p_fut_nc = netCDF4.Dataset('../bcsd3/sresa1b.%s.monthly.Prcp.1950-2099.nc' % (model,))

basets = datetime.datetime(1950,1,1)
days1 = (datetime.datetime(1981,1,1) - basets).days
days2 = (datetime.datetime(2000,1,1) - basets).days
days3 = (datetime.datetime(2046,1,1) - basets).days
days4 = (datetime.datetime(2065,1,1) - basets).days


offset1, offset2 = numpy.digitize([days1,days2], obs_nc.variables['time'][:])
offset3, offset4 = numpy.digitize([days3,days4], fut_nc.variables['time'][:])

output = open('../%s/monthly_deltas.csv' % (model,), 'w')
output.write("LON,LAT,JAN_T_DEL,FEB_T_DEL,MAR_T_DEL,APR_T_DEL,MAY_T_DEL,JUN_T_DEL,JUL_T_DEL,AUG_T_DEL,SEP_T_DEL,OCT_T_DEL,NOV_T_DEL,DEC_T_DEL,JAN_P_MUL,FEB_P_MUL,MAR_P_MUL,APR_P_MUL,MAY_P_MUL,JUN_P_MUL,JUL_P_MUL,AUG_P_MUL,SEP_P_MUL,OCT_P_MUL,NOV_P_MUL,DEC_P_MUL,\n")

pratio = numpy.zeros( (12, len(obs_nc.variables['latitude']), len(obs_nc.variables['longitude'])))
tdelta = numpy.zeros( (12, len(obs_nc.variables['latitude']), len(obs_nc.variables['longitude'])))

for i, mon in enumerate(["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL",
    "AUG", "SEP", "OCT", "NOV", "DEC"]):

    obs = numpy.average(obs_nc.variables['Tavg'][offset1+i:offset2:12,:,:],0)
    fut = numpy.average(fut_nc.variables['Tavg'][offset3+i:offset4:12,:,:],0)
    tdelta[i] = fut - obs
    p_obs = numpy.average(p_obs_nc.variables['Prcp'][offset1+i:offset2:12,:,:],0)
    p_fut = numpy.average(p_fut_nc.variables['Prcp'][offset3+i:offset4:12,:,:],0)
    pratio[i] = p_fut / p_obs


for row,lat in enumerate(obs_nc.variables['latitude'][:]):
    for col,lon in enumerate(obs_nc.variables['longitude'][:]):
        if lat < 31 or lat > 49 or lon < -110 or lon > -78:
            continue
        output.write("%f,%f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,\n" % (lon, lat, 
    tdelta[0,row,col], tdelta[1,row,col], tdelta[2,row,col], 
    tdelta[3,row,col], tdelta[4,row,col], tdelta[5,row,col], 
    tdelta[6,row,col], tdelta[7,row,col], tdelta[8,row,col], 
    tdelta[9,row,col], tdelta[10,row,col], tdelta[11,row,col], 
    pratio[0,row,col], pratio[1,row,col], pratio[2,row,col], 
    pratio[3,row,col], pratio[4,row,col], pratio[5,row,col], 
    pratio[6,row,col], pratio[7,row,col], pratio[8,row,col], 
    pratio[9,row,col], pratio[10,row,col], pratio[11,row,col]))

output.close()
