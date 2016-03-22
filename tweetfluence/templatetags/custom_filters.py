from django import template
from datetime import datetime
from math import trunc, ceil
import json

register = template.Library()


@register.filter
def evaluate_col_sm(value):
    if value < 2:
        return 'col-sm-12'
    elif value == 2 or value == 4:
        return 'col-sm-6'
    return 'col-sm-4'


@register.filter
def evaluate_col_xs(value):
    if value < 4:
        return 'col-xs-12'
    return 'col-xs-6'


@register.filter
def replace_spaces_with_dashes(value):
    return value.replace(' ', '-')


@register.filter
def trunc_int(value):
    return trunc(value)

@register.filter
def ceil_int(value):
    return ceil(value)

@register.filter
def is_float(value):
    return not (trunc(value) == value)


@register.filter
def get_range(value):
    return range(value)


@register.filter
def subtract_from(value, arg):
    return int(arg - value)

@register.filter
def json_dumps(value):
    return json.dumps(value)
