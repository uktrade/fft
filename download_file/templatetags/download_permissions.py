from django import template


register = template.Library()


@register.simple_tag
def has_oscar_download_permission(user):
    return user.has_perm("forecast.can_download_oscar")


@register.simple_tag
def has_mi_report_download_permission(user):
    return user.has_perm("forecast.can_download_mi_reports")


@register.simple_tag
def has_download_users_permission(user):
    return user.has_perm("user.can_download")
