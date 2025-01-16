from copy import copy
from typing import Iterator, TypedDict

from django import template

from forecast.models import FinancialPeriod


register = template.Library()


@register.filter("startswith")
def startswith(text, starts):
    return text.startswith(starts)


@register.filter
def instances_and_widgets(bound_field):
    """Allows the access of both model instance
    and form widget in template"""
    instance_widgets = []
    index = 0
    for instance in bound_field.field.queryset.all():
        widget = copy(bound_field[index])
        instance_widgets.append((instance, widget))
        index += 1
    return instance_widgets


@register.simple_tag
def has_end_of_month_archive_permissions(user):
    if user.is_superuser or user.groups.filter(name="Finance Administrator"):
        return True


class PreviousMonths(TypedDict):
    month_short_name = str
    month_financial_code = int


@register.simple_tag
def get_previous_months_data():
    def generator_data() -> Iterator[PreviousMonths]:
        qs = FinancialPeriod.objects.filter(actual_loaded=True).order_by(
            "financial_period_code"
        )
        for obj in qs:
            yield PreviousMonths(
                month_short_name=obj.period_short_name,
                month_financial_code=obj.financial_period_code,
            )

    return list(generator_data())
