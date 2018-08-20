from core.myutils import import_obj, IMPORT_CSV_MODEL_KEY, IMPORT_CSV_PK_KEY, IMPORT_CSV_FIELDLIST_KEY
from .models import DITPeople, Grade


PEOPLE_KEY = {IMPORT_CSV_MODEL_KEY: DepartmentalGroup,
             IMPORT_CSV_PK_KEY: 'GroupCode',
             'fieldlist' : {DepartmentalGroup.group_name.field_name: 'GroupName'}}


DIR_KEY = {IMPORT_CSV_MODEL_KEY: Directorate,
           IMPORT_CSV_PK_KEY: 'DirectorateCode',
           IMPORT_CSV_FIELDLIST_KEY: {Directorate.directorate_name.field_name: 'DirectorateDescription',
                                        Directorate.group.field.name: GROUP_KEY}}

CC_KEY = {IMPORT_CSV_MODEL_KEY: CostCentre,
          IMPORT_CSV_PK_KEY: 'CCCode',
          IMPORT_CSV_FIELDLIST_KEY: {CostCentre.cost_centre_name.field_name: 'CCDescription',
                                        CostCentre.active.field_name: 'Active',
                                        CostCentre.directorate.field.name: DIR_KEY}}


def import_cc(csvfile):
    import_obj(csvfile, CC_KEY)
