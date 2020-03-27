from django.core.exceptions import PermissionDenied


def has_download_oscar_permission(function):
    def wrap(view_func, *args, **kwargs):
        if view_func.request.user.has_perm("forecast.can_download_oscar"):
            return function(view_func, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def has_download_mi_report_permission(function):
    def wrap(view_func, *args, **kwargs):
        if view_func.request.user.has_perm("forecast.can_download_mi_report"):
            return function(view_func, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
