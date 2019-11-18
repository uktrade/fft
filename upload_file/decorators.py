from django.core.exceptions import PermissionDenied

from upload_file.models import UploadPermission


def has_upload_permission(function):
    def wrap(view_func, *args, **kwargs):
        upload_permissions = UploadPermission.objects.filter(
            user=view_func.request.user,
        ).first()

        if upload_permissions is not None:
            return function(view_func, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
