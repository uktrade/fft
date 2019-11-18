from django.core.exceptions import PermissionDenied

from forecast.models import ForecastPermission


def has_upload_permission(function):
    def wrap(view_func, *args, **kwargs):
        forecast_permissions = ForecastPermission.objects.filter(
            user=view_func.request.user,
        ).first()

        if forecast_permissions and forecast_permissions.can_upload:
            return function(view_func, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
