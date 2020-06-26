from django import template

register = template.Library()

def debug_var(value):
    # import pdb; pdb.set_trace()
    return ""

register.filter('debug', debug_var)