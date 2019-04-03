from .models import FinancialYear

def archive_generic(year, to_model, from_model):
    """It calls the archive function for the given model.
     It deletes the archived data for the same year, so it is possible to archive several time,
    if something was wrong the first time."""
    year_obj = FinancialYear.objects.get(financial_year=year)
    suffix =  ' (' + year_obj.financial_year_display + ')'
    # Delete the entries already in the table for the selected year
    if to_model.objects.filter(financial_year=year_obj).exists():
        to_model.objects.filter(financial_year=year_obj).delete()
    pc_qs = from_model.objects.all().select_related()
    for pc in pc_qs:
        to_model.archive_year(pc, year_obj, suffix)

