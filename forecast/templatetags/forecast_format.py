from django import template

from forecast.models import FinancialPeriod
from forecast.utils.view_header_definition import (
    budget_header,
    budget_spent_percentage_header,
    forecast_total_header,
    variance_header,
    variance_percentage_header,
    year_to_date_header,
)
register = template.Library()

forecast_figure_cols = [
    budget_header,
    year_to_date_header,
    forecast_total_header,
    variance_header,
]


@register.filter()
def is_forecast_figure(_, column):
    if str(column) in FinancialPeriod.financial_period_info.period_display_list() \
            or str(column) in forecast_figure_cols:
        return True

    return False


@register.filter()
def format_figure(value, column):
    if is_forecast_figure(value, column):
        try:
            figure_value = int(value) / 100
            return f'{round(figure_value):,d}'
        except ValueError:
            pass

    return value


@register.filter()
def is_percentage_figure(_, column):
    if str(column) == variance_percentage_header \
            or str(column) == budget_spent_percentage_header:
        return True

    return False


@register.filter()
def is_negative_percentage_figure(value, column):
    if str(column) == variance_percentage_header and value[:1] == '-':
        return True

    return False
