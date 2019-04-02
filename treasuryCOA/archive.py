
from core.models import FinancialYear
from .models import HistoricL5Account, L5Account

def archive_treasury_l5(year):
    """It copies the current tresury COA  hierarchy to a file. The hierarchy is flatten, and the historical table
    is not normalised. It deletes the archived data for the same year, so it is possible to archive several time,
    if something was wrong the first time."""
    year_obj = FinancialYear.objects.get(financial_year=year)
    suffix =  ' (' + year_obj.financial_year_display + ')'
    # Delete the entries already in the table for the selected year
    if HistoricL5Account.objects.filter(financial_year=year_obj).exists():
        HistoricL5Account.objects.filter(financial_year=year_obj).delete()
    l5_qs = L5Account.objects.all().select_related()
    for l5 in l5_qs:
        HistoricL5Account.archive_from_l5(l5, year_obj, suffix)


