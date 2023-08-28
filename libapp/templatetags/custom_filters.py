from django import template
from datetime import datetime

register = template.Library()

@register.filter(name='to_date')
def to_date(value):
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return None
