from django.core.exceptions import PermissionDenied

from forecast.utils.access_helpers import (
    can_download_mi_reports,
    can_download_oscar,
)


def has_download_oscar_permission(function):
    def wrap(view_func, *args, **kwargs):
        if can_download_oscar(view_func.request.user):
            return function(view_func, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def has_download_mi_report_permission(function):
    def wrap(view_func, *args, **kwargs):
        if can_download_mi_reports(view_func.request.user):
            return function(view_func, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
