from django import template

register = template.Library()

@register.filter(name='custom_debug')
def custom_debug(obj):
    return "Hi"
