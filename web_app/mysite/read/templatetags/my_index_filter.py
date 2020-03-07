from django import template

register = template.Library()

@register.filter(name='index')
def index(value, idx):
    return value[idx]
