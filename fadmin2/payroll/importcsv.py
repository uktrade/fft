from core.myutils import IMPORT_CSV_FIELDLIST_KEY, IMPORT_CSV_MODEL_KEY, IMPORT_CSV_PK_KEY, \
    import_obj

from .models import DITPeople

PEOPLE_KEY = {IMPORT_CSV_MODEL_KEY: DITPeople,
              IMPORT_CSV_PK_KEY: 'SE-No',
              IMPORT_CSV_FIELDLIST_KEY: {DITPeople.surname.field_name: 'Last Name',
                                         DITPeople.name.field_name: 'First Name', }}


def import_HR_Report(csvfile):
    import_obj(csvfile, PEOPLE_KEY)
