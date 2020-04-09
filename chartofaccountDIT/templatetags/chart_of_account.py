from django import template

register = template.Library()


@register.simple_tag
def financial_year(year):
    next_year = int(year) + 1
    return "{} - {}".format(
        year,
        next_year,
    )
