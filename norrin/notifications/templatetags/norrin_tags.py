import pprint

import humanize
from django import template


register = template.Library()


@register.filter(name='pprint')
def pprint_filter(value):
    pp = pprint.PrettyPrinter(indent=2)
    return pp.pformat(value)

@register.filter(name='naturaltime')
def naturaltime_filter(value):
    return humanize.naturaltime(value)
