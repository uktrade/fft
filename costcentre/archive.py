from core.models import FinancialYear
from .models import CostCentre, HistoricCostCentre

def archive_cost_centre(year):
    """It copies the current Cost Centre hierarchy to a file. The hierarchy is flatten, and the historical table
    is not normalised. It deletes the archived data for the same year, so it is possible to archive several time,
    if something was wrong the first time."""
    year_obj = FinancialYear.objects.get(financial_year=year)
    suffix =  ' (' + year_obj.financial_year_display + ')'
    # Delete the entries already in the table for the selected year
    if HistoricCostCentre.objects.filter(financial_year=year_obj).exists():
        HistoricCostCentre.objects.filter(financial_year=year_obj).delete()
    cc_qs = CostCentre.objects.all().select_related()
    for cc in cc_qs:
        HistoricCostCentre.archive_from_cc(cc, year_obj, suffix)


