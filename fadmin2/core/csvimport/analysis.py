from core.models import Analysis1, Analysis2
from core.myutils import import_obj


# define the column position in the csv file.

ANALYSIS1_KEY = {'model': Analysis1,
             'PK': Analysis1.Analysis1Code,
             Analysis1.Analysis1Code.field_name: 'Code',
             Analysis1.Analysis1Description.field_name: 'Description'}

ANALYSIS2_KEY = {'model': Analysis2,
             'PK': Analysis2.Analysis2Code,
             Analysis2.Analysis2Code.field_name: 'Code',
             Analysis2.Analysis2Description.field_name: 'Description'}

def import_Analysis1(csvfile):
    import_obj(csvfile, ANALYSIS1_KEY)

def import_Analysis2(csvfile):
    import_obj(csvfile, ANALYSIS2_KEY)

