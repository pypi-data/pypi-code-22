# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template import Library
from django.utils import six
from django.utils.encoding import force_text

register = Library()


@register.assignment_tag()
def get_type(value):
    if isinstance(value, six.string_types):
        return 'str'
    if value is None:
        return 'None'
    if isinstance(value, dict):
        return 'dict'
    if isinstance(value, bool):
        return 'bool'
    if isinstance(value, list):
        return 'list'
    if isinstance(value, int):
        return 'int'
    return force_text(type(value))
