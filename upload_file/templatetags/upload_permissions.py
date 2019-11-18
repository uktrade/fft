from django import template

from upload_file.models import UploadPermission

register = template.Library()


@register.simple_tag
def has_upload_permission(user):
    upload_permissions = UploadPermission.objects.filter(
        user=user,
    ).first()

    if upload_permissions is not None:
        return True

    return False
