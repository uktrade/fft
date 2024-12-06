from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.auth.models import Permission
from guardian.shortcuts import assign_perm as guardian_assign_perm


class NoForecastViewPermission(Exception):
    pass


def assign_perm(perm, user, cost_centre):
    # Check user can view forecasts

    if not user.has_perm("forecast.can_view_forecasts"):
        can_view_forecasts = Permission.objects.get(codename="can_view_forecasts")
        user.user_permissions.add(can_view_forecasts)
        user.save()

    LogEntry.objects.log_actions(
        user_id=user.id,
        action_flag=CHANGE,
        change_message="Cost Centre permission was assigned",
        single_object=True,
        queryset=[cost_centre],
    )

    guardian_assign_perm(perm, user, cost_centre)
