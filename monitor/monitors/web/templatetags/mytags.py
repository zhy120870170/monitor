# -*- coding: utf-8 -*-
from django import template
# 对象名必须为register
register = template.Library()


@register.filter()
@register.simple_tag()
def checkbox_is_selected(a1, a2):
    source_list = a1.split(",")
    if a2 in source_list:
        return "checked"
    else:
        return ""