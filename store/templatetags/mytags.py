'''
Created on 2020年12月24日

@author: Administrator
'''
from django import template

register = template.Library()

@register.filter(is_safe=True)
def label_with_classes(value, arg):
    return value.label_tag(attrs={'class': arg})

@register.filter(is_safe=True)
def label_with_styles(value, arg):
    return value.label_tag(attrs={'style': arg})

@register.filter()
def widget_with_classes(value, arg):
    return value.as_widget(attrs={'class': arg})