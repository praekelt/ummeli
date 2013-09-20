from django import template
from reporting import helpers
register = template.Library()

@register.simple_tag(takes_context=True)
def get_votes_for_object(context, obj, key):
    context[key] = helpers.get_object_votes(obj, key)
    return ''
