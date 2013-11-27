import datetime
import re

BILL_RE = re.compile(r"([a-z]+)(\d+)-\d+")
BILL_TYPES = {
    'hr': 'H.R.',
    'hres': 'H.Res.',
    'hjres': 'H.J.Res.',
    'hconres': 'H.Con.Res.',
    's': 'S.',
    'sres': 'S.Res.',
    'sjres': 'S.J.Res.',
    'sconres': 'S.Con.Res.',
}


def format_billid(bill_id):
    match = BILL_RE.match(bill_id)
    if match:
        groups = match.groups()
        return "%s %s" % (BILL_TYPES.get(groups[0], groups[0].upper()), groups[1])
    return bill_id


def today():
    dt = datetime.datetime.utcnow()
    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return dt


def day_before(dt):
    return dt - datetime.timedelta(days=1)


def yesterday():
    return day_before(today())
