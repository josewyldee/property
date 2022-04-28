from django import template
register = template.Library()

@register.simple_tag
def set_variable(val=None):
    print("ssssssssssss",val)

    return val