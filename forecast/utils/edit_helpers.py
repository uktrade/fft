from decimal import Decimal

from django.conf import settings

from core.myutils import get_current_financial_year
from core.utils import check_empty

from forecast.models import (
    FinancialPeriod,
    MonthlyFigure,
    MonthlyFigureAmount,
)


class CannotFindMonthlyFigureException(Exception):
    pass


class BadFormatException(Exception):
    pass


class RowMatchException(Exception):
    pass


class TooManyMatchException(Exception):
    pass


class NotEnoughMatchException(Exception):
    pass


class NoFinancialCodeForEditedValue(Exception):
    pass


def check_cols_match(cell_data):
    if len(cell_data) > 12 + settings.NUM_META_COLS:
        raise TooManyMatchException(
            'Your pasted data does not '
            'match the expected format. '
            'There are too many columns.'
        )
    if len(cell_data) < 12 + settings.NUM_META_COLS:
        raise NotEnoughMatchException(
            'Your pasted data does not '
            'match the expected format. '
            'There are not enough columns.'
        )


def get_monthly_figures(cost_centre_code, cell_data):
    start_period = FinancialPeriod.financial_period_info.actual_month() + 1
    monthly_figures = []

    for financial_period in range(start_period, 13):
        monthly_figure = MonthlyFigure.objects.filter(
            financial_code__cost_centre__cost_centre_code=cost_centre_code,
            financial_year__financial_year=get_current_financial_year(),
            financial_period__financial_period_code=financial_period,
            financial_code__programme__programme_code=check_empty(cell_data[1]),
            financial_code__natural_account_code__natural_account_code=cell_data[0],
            financial_code__analysis1_code=check_empty(cell_data[2]),
            financial_code__analysis2_code=check_empty(cell_data[3]),
            financial_code__project_code=check_empty(cell_data[4]),
        ).first()

        if not monthly_figure:
            raise CannotFindMonthlyFigureException(
                "Cannot one of the forecast figures, please contact"
                " a site administrator and include this text in your message"
            )

        col = (settings.NUM_META_COLS + financial_period) - 1
        new_value = convert_forecast_amount(cell_data[col])

        monthly_figure_amount = MonthlyFigureAmount.objects.filter(
            monthly_figure=monthly_figure,
        ).order_by("-version").first()

        if new_value != monthly_figure_amount.amount:
            MonthlyFigureAmount.objects.create(
                amount=new_value,
                monthly_figure=monthly_figure,
                version=monthly_figure_amount.version + 1
            )
            monthly_figures.append(monthly_figure)

    return monthly_figures


def check_row_match(index, pasted_at_row, cell_data):  # noqa C901
    if index != 0:
        return

    if not pasted_at_row:
        return

    mismatched_cols = []

    try:
        if pasted_at_row["natural_account_code"]["value"] != int(cell_data[0]):
            mismatched_cols.append('"Natural account code"')
    except ValueError:
        raise BadFormatException(
            "Your pasted data is not in the correct format"
        )

    if pasted_at_row["programme"]["value"] != cell_data[1]:
        mismatched_cols.append('"Programme"')

    if pasted_at_row["analysis1_code"]["value"] != check_empty(cell_data[2]):
        mismatched_cols.append('"Analysis 1"')

    if pasted_at_row["analysis2_code"]["value"] != check_empty(cell_data[3]):
        mismatched_cols.append('"Analysis 2"')

    if pasted_at_row["project_code"]["value"] != check_empty(cell_data[4]):
        mismatched_cols.append('"Project code"')

    if len(mismatched_cols) > 0:
        raise RowMatchException(
            "There is a mismatch between your pasted and selected"
            f" rows. Please check the following columns: {', '.join(mismatched_cols)}."
        )


def convert_forecast_amount(amount):
    return round(Decimal(amount.replace(",", ""))) * 100
