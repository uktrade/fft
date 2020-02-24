import calendar

from django import template

register = template.Library()

forecast_figure_cols = [
    "Budget",
    "Adjustment 1",
    "Adjustment 2",
    "Adjustment 3",
    "Year to Date",
    "Year Total",
    "Underspend (Overspend)",
]


@register.filter()
def is_forecast_figure(_, column):
    if str(column) in calendar.month_name or str(column) in forecast_figure_cols:
        return True

    return False


@register.filter()
def format_figure(value, column):
    if str(column) in calendar.month_name or str(column) in forecast_figure_cols:
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
