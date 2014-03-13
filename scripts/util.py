import datetime

def find_time_idx(nc, needle):
    ''' Find the time index '''
    tm = nc.variables['time']
    tstr = tm.units.replace("days since ", "")
    t0 = datetime.datetime.strptime(tstr.split()[0], '%Y-%m-%d')
    cal360 = True if tm.calendar == '360_day' else False
    cal365 = True if tm.calendar == '365_day' else False
    times = tm[:]
    for i, time in enumerate(times):
        if cal360:
            time = time - 15
            years = time / 360
            months = (time % 360 ) / 30
            ts = datetime.datetime(t0.year + years, 1 + months, 1)
        elif cal365:
            years = int( time / 365 )
            months = int((time % 365) / 30 )
            ts = datetime.datetime(t0.year + years, 1 + months, 1)
        else:
            ts = t0 + datetime.timedelta(days=time)
        if ts.year == needle.year and ts.month == needle.month:
            print 'Returning: %s/%s for needle: %s' % (i, len(times), needle)
            return i
    return None