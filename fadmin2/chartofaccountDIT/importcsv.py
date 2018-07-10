from .models import Analysis1, Analysis2
from core.myutils import import_obj, IMPORT_CSV_MODEL_KEY, IMPORT_CSV_PK_KEY, IMPORT_CSV_FIELDLIST_KEY



# define the column position in the csv file.

ANALYSIS1_KEY = {IMPORT_CSV_MODEL_KEY: Analysis1,
                 IMPORT_CSV_PK_KEY: 'Code',
                 IMPORT_CSV_FIELDLIST_KEY: {Analysis1.analysis1_description.field_name: 'Description'}}

ANALYSIS2_KEY = {IMPORT_CSV_MODEL_KEY: Analysis2,
                 IMPORT_CSV_PK_KEY: 'Code',
                 IMPORT_CSV_FIELDLIST_KEY: {Analysis2.analysis2_description.field_name: 'Description'}}


def import_Analysis1(csvfile):
    import_obj(csvfile, ANALYSIS1_KEY)

def import_Analysis2(csvfile):
    import_obj(csvfile, ANALYSIS2_KEY)

