from django import template

from forecast.permission_shortcuts import get_objects_for_user


register = template.Library()


@register.simple_tag
def is_forecast_user(user):
    return user.has_perm("forecast.can_view_forecasts")


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
