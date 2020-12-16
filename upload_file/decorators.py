from django.core.exceptions import PermissionDenied
from upload_file.utils import user_has_upload_permission


def has_upload_permission(function):
    def wrap(view_func, *args, **kwargs):
        if user_has_upload_permission(
            view_func.request.user,
        ):
            return function(view_func, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
