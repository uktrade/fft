import json

from django.conf import settings

from core.myutils import get_current_financial_year
from core.utils import check_empty

from forecast.models import (
    FinancialCode,
    FinancialPeriod,
    MonthlyFigure,
)


class CannotFindMonthlyFigureException(Exception):
    pass


class RowMatchException(Exception):
    pass


class ColMatchException(Exception):
    pass


def get_forecast_monthly_figures_pivot(cost_centre_code):

    pivot_filter = {"financial_code__cost_centre__cost_centre_code": "{}".format(
        cost_centre_code
    )}
    output = MonthlyFigure.pivot.pivot_data({}, pivot_filter)
    return list(output)


def check_cols_match(cell_data):
    if len(cell_data) != 12 + settings.NUM_META_COLS:
        raise ColMatchException(
            'Your pasted data does not '
            'match the expected format. '
            'There are not enough columns.'
        )


def get_monthly_figures(cost_centre_code, cell_data):
    start_period = FinancialPeriod.financial_period_info.actual_month() + 1
    monthly_figures = []

    financial_code = FinancialCode.objects.filter(
        cost_centre__cost_centre_code=cost_centre_code,
        programme__programme_code=check_empty(cell_data[1]),
        natural_account_code__natural_account_code=cell_data[0],
        analysis1_code=check_empty(cell_data[2]),
        analysis2_code=check_empty(cell_data[3]),
        project_code=check_empty(cell_data[4]),
    ).first()

    for financial_period in range(start_period, 13):
        monthly_figure = MonthlyFigure.objects.filter(
            financial_year__financial_year=get_current_financial_year(),
            financial_period__financial_period_code=financial_period,
            financial_code=financial_code,
        ).first()

        if not monthly_figure:
            raise CannotFindMonthlyFigureException(
                "Cannot find monthly figure"
            )

        new_value = int(cell_data[
            (settings.NUM_META_COLS + financial_period) - 1
        ])
        if new_value != monthly_figure.amount:
            monthly_figure.amount = new_value
            monthly_figures.append(monthly_figure)

    return monthly_figures


def check_row_match(index, pasted_at_row, cell_data):
    try:
        if index != 0:
            return

        if not pasted_at_row:
            return

        if (
            pasted_at_row[
                "natural_account_code"
            ]["value"] != int(cell_data[0]) or
            pasted_at_row[
                "programme"
            ]["value"] != cell_data[1] or
            pasted_at_row[
                "analysis1_code"
            ]["value"] != check_empty(cell_data[2]) or
            pasted_at_row[
                "analysis2_code"
            ]["value"] != check_empty(cell_data[3]) or
            pasted_at_row[
                "project_code"
            ]["value"] != check_empty(cell_data[4])
        ):
            raise RowMatchException(
                "Your pasted data does not match your selected row"
            )
    except Exception:
        raise RowMatchException(
            "Your pasted data is not in the correct format"
        )


def forecast_encoder(obj):
    print("WooWoo! Called!", obj)

    if isinstance(obj, int):
        return "{0:.2f}".format(obj)
    else:
        return obj
