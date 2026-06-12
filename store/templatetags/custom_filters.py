from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    """Multiplies value by arg"""
    try:
        return value * arg
    except (TypeError, ValueError):
        return 0