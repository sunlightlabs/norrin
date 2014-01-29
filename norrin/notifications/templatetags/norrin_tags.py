import pprint
from django import template


register = template.Library()


@register.filter(name='pprint')
def pprint_filter(value):
    pp = pprint.PrettyPrinter(indent=2)
    return pp.pformat(value)
