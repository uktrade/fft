from core.myutils import import_obj, IMPORT_CSV_MODEL_KEY, IMPORT_CSV_PK_KEY, IMPORT_CSV_FIELDLIST_KEY
from .models import DITPeople, Grade

PEOPLE_KEY = {IMPORT_CSV_MODEL_KEY: DITPeople,
              IMPORT_CSV_PK_KEY: 'SE-No',
              'fieldlist': {DITPeople.surname.field_name: 'Last Name',
                            DITPeople.name.field_name: 'First Name',
                            # DITPeople.cost_centre.field_name: 'CC',
                            # DITPeople.grade.field_name: 'Grade Level'
                            }}


def import_HR_Report(csvfile):
    import_obj(csvfile, PEOPLE_KEY)
