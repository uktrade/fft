from core.models import CostCentre, DepartmentalGroup, Directorate
from core.myutils import import_obj

# define the column position in the csv file.

# COLUMN_KEY = {
#                 'GroupCode': 3,
#                 'GroupName': 4,
#                 'DirectorateCode': 5,
#                 'DirectorateName': 6,
#                 'CCCode': 7,
#                 'CCName': 8}
#
#
# def importcostcentres(csvfile):
#     csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
#     for row in csvreader:
#         # Create DG Group, Directorate and Cost centre
#         objDG, created = DepartmentalGroup.objects.update_or_create(
#             GroupCode=row[COLUMN_KEY['GroupCode']],
#             defaults={'GroupName': row[COLUMN_KEY['GroupName']]},
#         )
#         objdir, created = Directorate.objects.update_or_create(
#             DirectorateCode=row[COLUMN_KEY['DirectorateCode']],
#             defaults={'GroupCode': objDG,
#                        'DirectorateName':row[COLUMN_KEY['DirectorateName']]},
#         )
#         obj, created = CostCentre.objects.update_or_create(
#             CCCode=row[COLUMN_KEY['CCCode']],
#             defaults={CostCentre.CCName.field_name: row[COLUMN_KEY['CCName']],
#                       CostCentre.Directorate.field.name: objdir},
#         )
#

GROUP_KEY = {'model': DepartmentalGroup,
             'PK': DepartmentalGroup.GroupCode,
             DepartmentalGroup.GroupCode.field_name: 'GroupCode',
             DepartmentalGroup.GroupName.field_name: 'GroupName'}


DIR_KEY = {'model': Directorate,
           'PK': Directorate.DirectorateCode,
           Directorate.DirectorateCode.field_name: 'DirectorateCode',
           Directorate.DirectorateName.field_name: 'DirectorateDescription',
           Directorate.GroupCode.field.name: GROUP_KEY}

CC_KEY = {'model': CostCentre,
          'PK': CostCentre.CCCode,
           CostCentre.CCCode.field_name: 'CCCode',
           CostCentre.CCName.field_name: 'CCDescription',
           CostCentre.Directorate.field.name: DIR_KEY}


def import_cc(csvfile):
    import_obj(csvfile, CC_KEY)
