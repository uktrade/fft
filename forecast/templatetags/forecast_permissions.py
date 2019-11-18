from django import template


from forecast.models import ForecastPermission
from forecast.permission_shortcuts import get_objects_for_user


register = template.Library()


@register.simple_tag
def is_forecast_user(user):
    forecast_permission = ForecastPermission.objects.filter(
        user=user,
    ).first()

    if forecast_permission:
        return True

    return False


@register.simple_tag
def has_edit_permission(user):
    # Find out if they have permissions on any cost centres
    cost_centres = get_objects_for_user(
        user,
        "costcentre.change_costcentre",
    )

    if cost_centres:
        return True

    return False
