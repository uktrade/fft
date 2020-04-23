from decimal import Decimal

from django.conf import settings

from core.myutils import get_current_financial_year
from core.utils import check_empty

from forecast.models import (
    FinancialCode,
    FinancialPeriod,
    ForecastMonthlyFigure,
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


def set_monthly_figure_amount(cost_centre_code, cell_data):
    start_period = FinancialPeriod.financial_period_info.actual_month() + 1

    period_max = FinancialPeriod.objects.filter(
        display_figure=True,
    ).count() + 1

    for financial_period_month in range(start_period, period_max):
        monthly_figure = ForecastMonthlyFigure.objects.filter(
            financial_code__cost_centre__cost_centre_code=cost_centre_code,
            financial_year__financial_year=get_current_financial_year(),
            financial_period__financial_period_code=financial_period_month,
            financial_code__programme__programme_code=check_empty(cell_data[0]),
            financial_code__natural_account_code__natural_account_code=cell_data[2],
            financial_code__analysis1_code=check_empty(cell_data[4]),
            financial_code__analysis2_code=check_empty(cell_data[5]),
            financial_code__project_code=check_empty(cell_data[6]),
        ).first()

        col = (settings.NUM_META_COLS + financial_period_month) - 1

        new_value = convert_forecast_amount(cell_data[col])

        if not monthly_figure:
            # Return if not required to make record
            if new_value == 0:
                return

            financial_code = FinancialCode.objects.get(
                cost_centre__cost_centre_code=cost_centre_code,
                programme__programme_code=check_empty(cell_data[0]),
                natural_account_code__natural_account_code=cell_data[2],
                analysis1_code=check_empty(cell_data[4]),
                analysis2_code=check_empty(cell_data[5]),
                project_code=check_empty(cell_data[6]),
            )
            financial_period = FinancialPeriod.objects.get(
                financial_period_code=financial_period_month,
            )
            monthly_figure = ForecastMonthlyFigure.objects.create(
                financial_year_id=get_current_financial_year(),
                financial_period=financial_period,
                financial_code=financial_code,
            )

        if new_value != monthly_figure.amount:
            monthly_figure.amount = new_value
            monthly_figure.save()


def check_row_match(index, pasted_at_row, cell_data):  # noqa C901
    if index != 0:
        return

    if not pasted_at_row:
        return

    mismatched_cols = []

    try:
        if pasted_at_row["programme"]["value"] != cell_data[0]:
            mismatched_cols.append('"Programme"')

        if pasted_at_row["natural_account_code"]["value"] != int(cell_data[2]):
            mismatched_cols.append('"Natural account code"')

        if pasted_at_row["analysis1_code"]["value"] != check_empty(cell_data[4]):
            mismatched_cols.append('"Analysis 1"')

        if pasted_at_row["analysis2_code"]["value"] != check_empty(cell_data[5]):
            mismatched_cols.append('"Analysis 2"')

        if pasted_at_row["project_code"]["value"] != check_empty(cell_data[6]):
            mismatched_cols.append('"Project code"')

    except (ValueError, IndexError):
        raise BadFormatException(
            "Your pasted data is not in the correct format"
        )

    if len(mismatched_cols) > 0:
        raise RowMatchException(
            "There is a mismatch between your pasted and selected"
            f" rows. Please check the following columns: {', '.join(mismatched_cols)}."
        )


def convert_forecast_amount(amount):
    return Decimal(amount.replace(",", "")) * 100


def check_cols_match(cell_data):
    return

    # TODO - reinstate the below when Luis has
    # added adjustment periods to edit spreadsheet downloads
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
