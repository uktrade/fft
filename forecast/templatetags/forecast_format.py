from django import template

from forecast.utils.view_header_definition import (
    budget_header,
    budget_spent_percentage_header,
    forecast_total_header,
    variance_header,
    variance_outturn_header,
    variance_percentage_header,
    year_to_date_header,
)


register = template.Library()

forecast_figure_cols = [
    budget_header,
    year_to_date_header,
    forecast_total_header,
    variance_header,
    variance_outturn_header,
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
    "Jan",
    "Feb",
    "Mar",
    "Adj1",
    "Adj2",
    "Adj3",
]


@register.filter
def format_money(value: float) -> str:
    """Format as a monetary value.

    `value` is expected to be in pence and will be divided by 100.

    Examples:
        >>> format_money(1024312)
        '10,243.12'
    """
    return f"{value / 100:,.2f}"


@register.filter()
def is_forecast_figure(_, column):
    if str(column) in forecast_figure_cols:
        return True

    return False


@register.filter()
def format_figure(value, column):
    if value and is_forecast_figure(value, column):
        try:
            figure_value = int(value) / 100
            return f"{round(figure_value):,d}"
        except ValueError:
            pass

    return value


@register.filter()
def is_percentage_figure(_, column):
    if (
        str(column) == variance_percentage_header
        or str(column) == budget_spent_percentage_header
    ):
        return True

    return False


@register.filter()
def is_negative_percentage_figure(value, column):
    if str(column) == variance_percentage_header and value[:1] == "-":
        return True

    return False
