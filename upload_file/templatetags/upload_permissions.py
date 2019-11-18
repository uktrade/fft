from django import template

from forecast.models import ForecastPermission


register = template.Library()


@register.simple_tag
def has_upload_permission(user):
    forecast_permission = ForecastPermission.objects.filter(
        user=user,
    ).first()

    if forecast_permission and forecast_permission.can_upload:
        return True

    return False
