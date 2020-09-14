from django import template

register = template.Library()


@register.simple_tag
def has_end_of_month_archive_permission(user):
    return user.has_perm("forecast.can_archive_end_of_month")
