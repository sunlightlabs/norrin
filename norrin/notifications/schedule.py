import datetime
import pytz

# start and end times
# in US/Eastern
DND_START = (0, 0)  # 0:00
DND_END = (8, 30)   # 8:30

EASTERN = pytz.timezone('US/Eastern')



def eastern_datetime(h, m, date=None):
    if not date:
        date = datetime.datetime.today()
    time = datetime.time(h, m, 0, 0, tzinfo=EASTERN)
    dt = datetime.datetime.combine(date, time)
    return dt


def is_dnd(dt):
    dnd_start = eastern_datetime(*DND_START).astimezone(pytz.utc)
    dnd_end = eastern_datetime(*DND_END).astimezone(pytz.utc)
    return dnd_start <= dt < dnd_end


def disturbable_datetime(dt=None, tz=pytz.utc):

    if dt:
        # convert to utc
        dt = dt.astimezone(pytz.utc)
    else:
        # create utc from local time
        dt = datetime.datetime.now(pytz.utc).replace(second=0, microsecond=0)

    if is_dnd(dt):
        date = dt.date()
        time = datetime.time(*DND_END, tzinfo=EASTERN)
        dt = datetime.datetime.combine(date, time)

    if tz:
        dt = dt.astimezone(tz)
        dt = tz.localize(dt)
    else:
        dt = dt.replace(tzinfo=None)

    return dt





if __name__ == '__main__':

    dnd_dt = eastern_datetime(*DND_END).astimezone(pytz.utc)


    dt = datetime.datetime(2014, 7, 1, 4, 0, 0, tzinfo=EASTERN)
    dt = disturbable_datetime(dt, tz=EASTERN)
    value = dt.isoformat()
    expected = '2014-08-05 04:00:00'
    print value, expected, value == expected


    # now = datetime.datetime.utcnow()
    # dnd_time = datetime.time(5, 0, 0, 0)
    # nondnd_time = datetime.time(10, 0, 0, 0)

    # print is_dnd(now)
    # print is_dnd(dnd_time)
    # print is_dnd(nondnd_time)
