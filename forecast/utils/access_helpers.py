from datetime import date

from guardian.shortcuts import (
    get_objects_for_user as guardian_get_objects_for_user,
)

from costcentre.models import (
    CostCentre,
)

from forecast.models import (
    ForecastEditState,
    UnlockedForecastEditor,
)


def can_view_forecasts(user):
    """Checks view permission, if the user can edit ANY
    cost centre, they are allowed to view ALL forecasts"""
    if can_edit_at_least_one_cost_centre(
        user
    ):
        return True

    return user.has_perm(
        "forecast.can_view_forecasts"
    )


def is_system_locked():
    forecast_edit_date = ForecastEditState.objects.get()

    if (
        forecast_edit_date.lock_date and date.today() >= forecast_edit_date.lock_date
    ):
        return True

    return False


def is_system_closed():
    forecast_edit_date = ForecastEditState.objects.get()

    if forecast_edit_date.closed:
        return True

    return False


def user_in_group(user, group):
    return user.groups.filter(
        name=group,
    ).exists()


def can_edit_at_least_one_cost_centre(user):
    if user.is_superuser or user.has_perm(
        "costcentre.edit_forecast_all_cost_centres"
    ):
        return True

    cost_centres = guardian_get_objects_for_user(
        user,
        "change_costcentre",
        klass=CostCentre,
        accept_global_perms=False,
    )

    return cost_centres.count() > 0


def get_user_cost_centres(user):
    if user.is_superuser or user.has_perm(
        "costcentre.edit_forecast_all_cost_centres"
    ):
        return CostCentre.objects.all()

    return guardian_get_objects_for_user(
        user,
        "costcentre.change_costcentre",
        accept_global_perms=False,
    )


def can_forecast_be_edited(user):
    if user.is_superuser:
        return True

    closed = is_system_closed()
    locked = is_system_locked()

    if not closed and not locked:
        return True

    if user.has_perm("forecast.can_edit_whilst_locked"):
        return True

    if closed and not locked and user.has_perm("forecast.can_edit_whilst_closed"):
        return True

    if UnlockedForecastEditor.objects.filter(
        user=user,
    ).exists():
        return True

    return False


def can_edit_cost_centre(user, cost_centre_code):
    if user.has_perm(
        "costcentre.edit_forecast_all_cost_centres"
    ):
        return True

    cost_centre = CostCentre.objects.get(
        cost_centre_code=cost_centre_code,
    )

    return user.has_perm(
        "costcentre.change_costcentre",
        cost_centre,
    )


def can_download_mi_reports(user):
    return user.has_perm("forecast.can_download_mi_reports")


def can_download_oscar(user):
    return user.has_perm("forecast.can_download_oscar")
