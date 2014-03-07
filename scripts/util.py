import datetime

def find_time_idx(nc, needle):
    ''' Find the time index '''
    tm = nc.variables['time']
    t0 = datetime.datetime.strptime(tm.units.replace("days since ", ""), '%Y-%m-%d')
    cal365 = True if tm.calendar == '360_day' else False
    times = tm[:]
    for i, time in enumerate(times):
        if cal365:
            time = time - 15
            years = time / 360
            months = (time % 360 ) / 30
            ts = datetime.datetime(t0.year + years, 1 + months, 1)
        else:
            ts = t0 + datetime.timedelta(days=time)
        if ts.year == needle.year and ts.month == needle.month:
            return i
    return None