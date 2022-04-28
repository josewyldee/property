from django import template
register = template.Library()

@register.simple_tag
def setvar(val):
  return val