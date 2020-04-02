from django import template

from costcentre.models import CostCentre

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


@register.simple_tag
def has_cost_centre_edit_permission(user, cost_centre_code):
    # Find out if they have permission on a specific cost centre
    cost_centre = CostCentre.objects.get(cost_centre_code=cost_centre_code)

    return user.has_perm("change_costcentre", cost_centre)
