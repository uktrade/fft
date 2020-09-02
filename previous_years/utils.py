from core.models import FinancialYear


def valid_year_for_archiving_actuals(financial_year):
    # check that the chart of account has been archived.
    # otherwise, every single row of the uploaded file will generate an error
    try:
        obj = FinancialYear.objects.get(pk=financial_year)
    except FinancialYear.DoesNotExist:
        return False

    # Checks if there are cost centres archived for this year
    # and all the mandatory members of the Chart of Account
    if (
        obj.chartofaccountdit_archivednaturalcode.all().count()
        & obj.chartofaccountdit_archivedprogrammecode.all().count()
        & obj.costcentre_archivedcostcentre.all().count()
    ):
        return True
    return False
