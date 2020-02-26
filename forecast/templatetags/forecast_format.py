from django import template

from forecast.models import FinancialPeriod

register = template.Library()

forecast_figure_cols = [
    "Budget",
    "Year to Date",
    "Year Total",
    "Underspend (Overspend)",
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
    if str(column) == '%':
        return True

    return False


@register.filter()
def is_negative_percentage_figure(value, column):
    if str(column) == '%' and value[:1] == '-':
        return True

    return False
