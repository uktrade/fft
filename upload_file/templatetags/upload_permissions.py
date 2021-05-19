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


@register.simple_tag
def has_project_percentage_permission(user):
    if user.is_superuser:
        return True
    elif user.has_perm(
        "split_project.can_upload_files"
    ) or user.groups.filter(
        name="Finance Administrator"
    ):
        return True
    else:
        return False
