from core.models import FinancialYear
from core.utils.generic_helpers import get_current_financial_year


class ArchiveYearError(Exception):
    pass


def validate_year_for_archiving(financial_year):
    current_year = get_current_financial_year()
    if financial_year == current_year:
        raise (ArchiveYearError(f"{financial_year} is the current year."))

    if financial_year == current_year:
        raise (ArchiveYearError(f"{financial_year} is in the future."))

    try:
        obj = FinancialYear.objects.get(pk=financial_year)
    except FinancialYear.DoesNotExist:
        raise (ArchiveYearError(f"Financial year {financial_year} does not exist."))
    return obj


def validate_year_for_archiving_actuals(financial_year):
    obj = validate_year_for_archiving(financial_year)

    # Checks if there are cost centres archived for this year
    # and all the mandatory members of the Chart of Account
    # check that the chart of account has been archived.
    # otherwise, every single row of the uploaded file will generate an error
    error_found = False
    error_msg = ""
    if obj.costcentre_archivedcostcentre.all().count() == 0:
        error_found = True
        error_msg = "No cost centres available. "

    if obj.chartofaccountdit_archivednaturalcode.all().count() == 0:
        error_found = True
        error_msg = f"{error_msg}No natural account code available. "

    if obj.chartofaccountdit_archivedprogrammecode.all().count() == 0:
        error_found = True
        error_msg = f"{error_msg}No programme code available. "

    if error_found:
        raise (
            ArchiveYearError(
                f"Error(s) in chart of account for {financial_year}: f{error_msg}"
            )
        )
