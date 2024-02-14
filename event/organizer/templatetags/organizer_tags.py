from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='get_description')
@stringfilter
def get_type(mapping, key):
    thismap = { 
        "statistics" : "View the Statistics for This Years Event",
        "display-hackers" : "View All of the Registered Hackers"
    }
    return thismap[key]