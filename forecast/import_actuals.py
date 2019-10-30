from openpyxl import load_workbook

from chartofaccountDIT.models import (
    Analysis1,
    Analysis2,
    NaturalCode,
    ProgrammeCode,
    ProjectCode,
)

from core.import_csv import get_fk, get_fk_from_field
from core.models import FinancialYear

from costcentre.models import CostCentre

from forecast.models import (
    FinancialPeriod,
    MonthlyFigure,
)

CHART_OF_ACCOUNT_COL = "D"
ACTUAL_FIGURE_COL = "F"
NAC_COL = "A"

FIRST_DATA_ROW = 13

MONTH_CELL = "B2"
TITLE_CELL = "B1"
CORRECT_TITLE = "Detail Trial Balance"

# Sample chart of account entry
# '3000-30000-109189-52191003-310940-00000-00000-0000-0000-0000' # noqa
# The following are the index for the
# chart of account after decoded into a list
DIT_INDEX = (
    0
)  # col value must be 3000. If not, the trial balance is for another department # noqa
CC_INDEX = 2
NAC_INDEX = 3
PROGRAMME_INDEX = 4
ANALYSIS1_INDEX = 5
ANALYSIS2_INDEX = 6
PROJECT_INDEX = 7
CHART_ACCOUNT_SEPARATOR = "-"

# TODO Read the value from the database. It should be possible for the business to change it. # noqa
GENERIC_PROGRAMME_CODE = 310940


class SubTotalFieldDoesNotExistError(Exception):
    pass


class SubTotalFieldNotSpecifiedError(Exception):
    pass


def check_trial_balance_format(ws, period, year):
    """Check that the file is really the trial
    balance and it is the correct period"""
    if ws.title != "FNDWRR":
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

    return True


def get_chart_account_obj(model, chart_of_account_item):
    if int(chart_of_account_item):
        obj, message = get_fk(model, chart_of_account_item)
    else:
        obj = None
        message = ""
    return obj, message


def save_row(chart_of_account, value, period_obj, year_obj):
    """Parse the long strings containing the
    chart of account information. Return errors
    if missing from database."""
    # Sample line:
    # '3000-30000-109189-52191003-310940-00000-00000-0000-0000-0000' # noqa
    chart_account_list = chart_of_account.split(CHART_ACCOUNT_SEPARATOR)
    programme_code = chart_account_list[PROGRAMME_INDEX]
    # Handle lines without programme code
    if not int(programme_code):
        if value:
            programme_code = GENERIC_PROGRAMME_CODE
        else:
            return True, ""

    # TODO Check that the NAC is resource or capital
    error_message = ""
    cc_obj, message = get_fk(CostCentre, chart_account_list[CC_INDEX])
    error_message += message
    nac_obj, message = get_fk(NaturalCode, chart_account_list[NAC_INDEX])
    error_message += message
    programme_obj, message = get_fk(ProgrammeCode, programme_code)
    error_message += message
    analysis1_obj, message = get_chart_account_obj(Analysis1,
                                                   chart_account_list[ANALYSIS1_INDEX])
    error_message += message
    analysis2_obj, message = get_chart_account_obj(Analysis2,
                                                   chart_account_list[ANALYSIS2_INDEX])
    error_message += message
    project_obj, message = get_chart_account_obj(ProjectCode,
                                                 chart_account_list[PROJECT_INDEX])
    error_message += message

    if error_message == "":
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
        if created:
            # to avoid problems with precision, we store the figures in pence
            monthly_figure_obj.amount = value * 100
        else:
            monthly_figure_obj.amount += value * 100
        monthly_figure_obj.save()
        success = True
    else:
        success = False
    return success, error_message


def upload_trial_balance_report(path, month_number, year):
    wb = load_workbook(path, read_only=True)
    ws = wb.worksheets[0]
    if not check_trial_balance_format(ws, month_number, year):
        wb.close
        return
    """TODO Use transactions, so it can rollback if there is an error in the file"""
    year_obj, msg = get_fk(FinancialYear, year)
    period_obj, msg = get_fk_from_field(
        FinancialPeriod,
        "period_calendar_code",
        month_number)
    # Delete the existing actuals.
    # There are multiple lines in the Trial Balance for the same combination of Chart-of-Account,
    # so we need to add the figures when we save them. This means that we need to start with a clean slate.
    MonthlyFigure.objects.filter(
        financial_year=year,
        financial_period=period_obj).delete()

    for row in range(FIRST_DATA_ROW, ws.max_row):
        chart_of_account = ws["{}{}".format(CHART_OF_ACCOUNT_COL, row)].value
        if chart_of_account:
            actual = ws["{}{}".format(ACTUAL_FIGURE_COL, row)].value
            if actual:
                save_row(chart_of_account, actual, period_obj, year_obj)
        else:
            break

    period_obj.actual_loaded = True
    period_obj.save()
#     TODO log date and time of upload
