from .models import Analysis1, Analysis2
from core.myutils import import_obj


# define the column position in the csv file.

ANALYSIS1_KEY = {'model': Analysis1,
             'PK': Analysis1.analysis1_code,
             Analysis1.analysis1_code.field_name: 'Code',
             Analysis1.analysis1_description.field_name: 'Description'}

ANALYSIS2_KEY = {'model': Analysis2,
             'PK': Analysis2.analysis2_code,
             Analysis2.analysis2_code.field_name: 'Code',
             Analysis2.analysis2_description.field_name: 'Description'}

def import_Analysis1(csvfile):
    import_obj(csvfile, ANALYSIS1_KEY)

def import_Analysis2(csvfile):
    import_obj(csvfile, ANALYSIS2_KEY)

