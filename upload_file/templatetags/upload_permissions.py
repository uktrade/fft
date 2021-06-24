from django import template

register = template.Library()


@register.simple_tag
def has_upload_permission(user):
    return user.has_perm("forecast.can_upload_files") or user.groups.filter(
        name="Finance Administrator"
    )


@register.simple_tag
def has_admin_upload_permission(user):
    return user.has_perm("upload_file.can_upload_admin")
