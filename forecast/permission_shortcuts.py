from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from guardian.shortcuts import (
    assign_perm as guardian_assign_perm,
    get_objects_for_user as guardian_get_objects_for_user,
)


class NoForecastViewPermission(Exception):
    pass


def assign_perm(perm, user, cost_centre):
    # Check user can view forecasts

    if not user.has_perm("forecast.can_view_forecasts"):
        can_view_forecasts = Permission.objects.get(codename='can_view_forecasts')
        user.user_permissions.add(can_view_forecasts)
        user.save()

    LogEntry.objects.log_action(
        user_id=user.id,
        content_type_id=ContentType.objects.get_for_model(cost_centre).pk,
        object_id=cost_centre.cost_centre_code,
        object_repr=cost_centre.cost_centre_name,
        action_flag=CHANGE,
        change_message="Cost Centre permission was assigned",
    )

    guardian_assign_perm(perm, user, cost_centre)


def get_objects_for_user(user, perms, *args, **kwargs):
    # Check user can view forecasts
    if not user.has_perm("forecast.can_view_forecasts"):
        raise NoForecastViewPermission(
            "Users without forecast view "
            "permission cannot edit cost centres"
        )

    return guardian_get_objects_for_user(user, perms, *args, **kwargs)
