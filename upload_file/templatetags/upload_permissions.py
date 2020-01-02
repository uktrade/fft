from django import template

register = template.Library()


@register.simple_tag
def has_upload_permission(user):
    return user.has_perm("forecast.can_upload_files")
