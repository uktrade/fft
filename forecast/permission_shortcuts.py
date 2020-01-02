from django.contrib.auth.models import Permission

from guardian.shortcuts import (
    assign_perm as guardian_assign_perm,
    get_objects_for_user as guardian_get_objects_for_user,
)


class NoForecastViewPermission(Exception):
    pass


def assign_perm(perm, user, *args, **kwargs):
    # Check user can view forecasts

    if not user.has_perm("forecast.can_view_forecasts"):
        can_view_forecasts = Permission.objects.get(codename='can_view_forecasts')
        user.user_permissions.add(can_view_forecasts)
        user.save()

    guardian_assign_perm(perm, user, *args, **kwargs)


def get_objects_for_user(user, perms, *args, **kwargs):
    # Check user can view forecasts
    if not user.has_perm("forecast.can_view_forecasts"):
        raise NoForecastViewPermission(
            "Users without forecast view "
            "permission cannot edit cost centres"
        )

    return guardian_get_objects_for_user(user, perms, *args, **kwargs)
