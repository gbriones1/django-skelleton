from django import template

register = template.Library()

@register.filter(name='custom_debug')
def custom_debug(obj):
    return "Hi"

@register.filter(name='inspect')
def inspect(obj):
    import pdb; pdb.set_trace()
