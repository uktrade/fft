from chartofaccountDIT.importcsv import import_Analysis1, import_Analysis2, import_NAC, \
    import_NAC_DIT, import_NAC_category,  \
    import_NAC_expenditure_category, \
    import_commercial_category, \
    import_expenditure_category, import_programme

from costcentre.importcsv import import_cc

from django.core.management.base import BaseCommand

from forecast.importcsv import import_adi_file, import_unpivot_actual

from payroll.importcsv import import_HR_Report

from treasuryCOA.importcsv import import_treasury_COA

IMPORT_TYPE = {
    'CostCentre': import_cc,
    # 'Segments' : import_treasury_segments,
    'Treasury_COA': import_treasury_COA,
    'Programmes': import_programme,
    'NAC': import_NAC,  # import from the BICC file
    'Analysis1': import_Analysis1,
    'Analysis2': import_Analysis2,
    'NAC_Dashboard_Group': import_NAC_expenditure_category,
    'NAC_Dashboard_Budget': import_expenditure_category,
    'NAC_Category': import_NAC_category,
    'NAC_DIT_Setting': import_NAC_DIT,  # add extra fields defined by DIT
    'HR_Report': import_HR_Report,
    'NAC_Dashboard_other': import_expenditure_category,
    'Commercial_Cat': import_commercial_category,
    'ADI': import_adi_file
}


class Command(BaseCommand):
    help = 'Import data from csv file'

    def add_arguments(self, parser):
        parser.add_argument('csv_path')
        parser.add_argument('type')
        parser.add_argument('year', type=int, nargs='?', default=None)
        parser.add_argument('month', nargs='?', default=None)

    # pass the file path as an argument
    # second argument will define the content of the file
    # importing actual is a special case, because we need to specify the month
    def handle(self, *args, **options):
        path = options.get('csv_path')
        print(path)
        importtype = options.get('type')
        # Windows-1252 or CP-1252, used because of a back quote
        csvfile = open(path, newline='', encoding='cp1252')
        if importtype == 'UnPivotActuals':
            financialyear = options.get('year')
            import_unpivot_actual(csvfile, financialyear)
        else:
            IMPORT_TYPE[importtype](csvfile)
        csvfile.close()
