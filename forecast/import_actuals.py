from openpyxl import load_workbook

from chartofaccountDIT.models import (
    Analysis1,
    Analysis2,
    NaturalCode,
    ProgrammeCode,
    ProjectCode
)

from core.import_csv import get_fk
from costcentre.models import CostCentre
from .models import MonthlyFigure


CHART_OF_ACCOUNT_COL = 'D'
MONTHLY_FIGURE_COL = 'F'
NAC_COL = 'A'

FIRST_DATA_ROW = 13

MONTH_CELL = 'B2'
TITLE_CELL = 'B1'
CORRECT_TITLE = 'Detail Trial Balance'

# Sample chart of account entry
# '3000-30000-109189-52191003-310940-00000-00000-0000-0000-0000' # noqa
# The following are the index for the
# chart of account after decoded into a list
DIT_INDEX = 0  # col value must be 3000. If not, the trial balance is for another department # noqa
CC_INDEX = 2
NAC_INDEX = 3
PROGRAMME_INDEX = 4
ANALYSIS1_INDEX = 5
ANALYSIS2_INDEX = 6
PROJECT_INDEX = 7
CHART_ACCOUNT_SEPARATOR = '-'


class SubTotalFieldDoesNotExistError(Exception):
    pass


class SubTotalFieldNotSpecifiedError(Exception):
    pass


def check_trial_balance_format(file, period):
    """Check that the file is really the trial
    balance and it is the correct period"""
    pass


def row_to_use(row):
    """Check the account code: if resource or
    capital use the row, otherwise ignore it"""
    if row[MONTHLY_FIGURE_COL] == 0:
        return False
    # if row[NAC_COL] not resouce:
    #     return False
    return True


def save_row(
    chart_of_account,
    value,
    period_obj,
    year_obj,
):
    """Parse the long strings containing the
    chart of account information. Return errors
    if missing from database."""
    # '3000-30000-109189-52191003-310940-00000-00000-0000-0000-0000' # noqa
    chart_account_list = chart_of_account[
        CHART_OF_ACCOUNT_COL
    ].split(
        CHART_ACCOUNT_SEPARATOR
    )
    error_message = ''
    cc_obj, message = get_fk(
        CostCentre,
        chart_account_list[CC_INDEX],
    )
    error_message += message
    nac_obj, message = get_fk(
        NaturalCode,
        chart_account_list[NAC_INDEX],
    )
    error_message += message
    programme_obj, message = get_fk(
        ProgrammeCode,
        chart_account_list[PROGRAMME_INDEX],
    )
    error_message += message
    analysis1_obj, message = get_fk(
        Analysis1,
        chart_account_list[ANALYSIS1_INDEX],
    )
    error_message += message
    analysis2_obj, message = get_fk(
        Analysis2,
        chart_account_list[ANALYSIS2_INDEX],
    )
    error_message += message
    project_obj, message = get_fk(
        ProjectCode,
        chart_account_list[PROJECT_INDEX],
    )

    if error_message == '':
        monthly_figure_obj, created = MonthlyFigure.objects.get_or_create(
            financial_year=year_obj,
            programme=programme_obj,
            cost_centre=cc_obj,
            natural_account_code=nac_obj,
            analysis1_code=analysis1_obj,
            analysis2_code=analysis2_obj,
            project_code=project_obj,
            financial_period=period_obj,
        )
        # to avoid problems with precision, we store the figures in pence
        monthly_figure_obj.amount = value * 100
        monthly_figure_obj.save()
        success = True
    else:
        success = False
    return success, error_message


def upload_file(path, period, year):
    """Use transactions, so it can rollback
    if there is an error in the file"""
    wb = load_workbook(path)
    ws = wb.worksheets[0]
    if ws.title != 'FNDWRR':
        # wrong file
        return False
    if ws[TITLE_CELL].value != CORRECT_TITLE:
        # wrong file
        return False

    report_date = ws[MONTH_CELL].value
    if report_date.year != year:
        # wrong date
        return False

    if report_date.month != period:
        # wrong date
        return False

    # If we are here, the file is a trial balance
    # run for the correct period
    # ws.cell(row=i, column=1).value
