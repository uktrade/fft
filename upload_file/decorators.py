from django.core.exceptions import PermissionDenied


def has_upload_permission(function):
    def wrap(view_func, *args, **kwargs):
        if view_func.request.user.has_perm(
                "forecast.can_upload_files"
        ) or view_func.request.user.groups.filter(
            name="Finance Administrator"
        ):
            return function(view_func, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
