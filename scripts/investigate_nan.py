'''
 Investigate issues with NAN?
'''
import netCDF4
import numpy as np
import numpy.ma as ma
import datetime
import glob
import os

os.chdir("/tera13/akrherz/hayhoe")
files = glob.glob("*tmax*")
files.sort()
for fn in files:
    tasmax_nc = netCDF4.Dataset( fn )
    
    tokens = (tasmax_nc.variables['time'].units).replace("days since ", "").split("-")
    basets = datetime.datetime( int(tokens[0]), int(tokens[1]), int(tokens[2]) )
    
    bad = 0
    for k, tm in enumerate(tasmax_nc.variables['time'][:]):
        m = np.max(tasmax_nc.variables['tmax'][k,:,:])
        if ma.is_masked(m):
            bad += 1
            #ts = basets + datetime.timedelta(days=int(tm))
            #print ts.strftime("%Y-%m-%d")
        
    print '%5s/%5s %5.2f%% %s' % (bad, k+1, bad / float(k+1) * 100.0, fn)
        
    tasmax_nc.close()

