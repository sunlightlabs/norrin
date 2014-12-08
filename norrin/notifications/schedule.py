import datetime
import pytz

UTC = pytz.utc
DC = pytz.timezone('US/Eastern')

# in US/Eastern
DND_START = datetime.time(1, 0, 0)
DND_END = datetime.time(8, 30, 0)


def today_time(time, date=None, tz=None):
    if not date:
        date = datetime.date.today()
    if not tz:
        tz = UTC
    dt = datetime.datetime.combine(date, time)
    dt = tz.localize(dt)
    return dt


def delay_until_local():
    now = datetime.datetime.now(UTC)
    start = today_time(DND_START, tz=DC).astimezone(UTC)
    end = today_time(DND_END, tz=DC).astimezone(UTC)
    if start < now < end:
        return today_time(DND_END, tz=DC).replace(tzinfo=None)


if __name__ == '__main__':

    print delay_until_local()

