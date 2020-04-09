from django import template

from forecast.utils.access_helpers import (
    can_edit_at_least_one_cost_centre as can_edit_at_least_one_cost_centre_helper,
    can_edit_cost_centre as can_edit_cost_centre_helper,
    can_view_forecasts,
)


register = template.Library()


@register.simple_tag
def is_forecast_user(user):
    return can_view_forecasts(user)


@register.simple_tag
def can_edit_at_least_one_cost_centre(user):
    return can_edit_at_least_one_cost_centre_helper(user)


@register.simple_tag
def can_edit_cost_centre(user, cost_centre_code):
    return can_edit_cost_centre_helper(user, cost_centre_code)
