from guardian.shortcuts import (
    assign_perm as guardian_assign_perm,
    get_objects_for_user as guardian_get_objects_for_user,
)

from forecast.models import ForecastPermission


class NoForecastViewPermission(Exception):
    pass


def assign_perm(perm, user, *args, **kwargs):
    # Check user can view forecasts
    forecast_permission = ForecastPermission.objects.filter(
        user=user,
    ).first()

    if not forecast_permission:
        # Add forecast permission
        forecast_permission = ForecastPermission(
            user=user,
        )
        forecast_permission.save()

    guardian_assign_perm(perm, user, *args, **kwargs)


def get_objects_for_user(user, perms, *args, **kwargs):
    # Check user can view forecasts
    forecast_permission = ForecastPermission.objects.filter(
        user=user,
    ).first()

    if not forecast_permission:
        raise NoForecastViewPermission(
            "Users without forecast view "
            "permission cannot edit cost centres"
        )

    return guardian_get_objects_for_user(user, perms, *args, **kwargs)
