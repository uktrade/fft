import csv

from core.myutils import IMPORT_CSV_FIELDLIST_KEY, IMPORT_CSV_MODEL_KEY, \
    IMPORT_CSV_PK_KEY, ImportInfo, csvheadertodict, import_obj


from .models import BSCEEmail, BusinessPartner, \
    CostCentre, CostCentrePerson, DepartmentalGroup, Directorate

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

GROUP_KEY = {IMPORT_CSV_MODEL_KEY: DepartmentalGroup,
             IMPORT_CSV_PK_KEY: 'GroupCode',
             'fieldlist': {DepartmentalGroup.group_name.field_name: 'GroupName'}}

DIR_KEY = {IMPORT_CSV_MODEL_KEY: Directorate,
           IMPORT_CSV_PK_KEY: 'DirectorateCode',
           IMPORT_CSV_FIELDLIST_KEY:
               {Directorate.directorate_name.field_name: 'DirectorateDescription',
                Directorate.group.field.name: GROUP_KEY}}

CC_KEY = {IMPORT_CSV_MODEL_KEY: CostCentre,
          IMPORT_CSV_PK_KEY: 'CCCode',
          IMPORT_CSV_FIELDLIST_KEY: {CostCentre.cost_centre_name.field_name: 'CCDescription',
                                     CostCentre.active.field_name: 'Active',
                                     CostCentre.directorate.field.name: DIR_KEY}}


def import_cc(csvfile):
    import_obj(csvfile, CC_KEY)


import_cc_class = ImportInfo(CC_KEY, 'Departmental Groups, Directorates and Cost Centres')


def import_cc_responsibles(csvfile):
    """Special function to import the Deputy Director,  Business partner and BSCE email"""
    reader = csv.reader(csvfile)
    # Convert the first row to a dictionary of positions
    header = csvheadertodict(next(reader))
    for row in reader:
        obj  = CostCentre.objects.get(
            pk=row[header['CC Code']].strip())
        deputy_obj, created = CostCentrePerson.objects.get_or_create(name=row[header['Deputy Name']].strip(),
                                              surname=row[header['Deputy Surname']].strip())
        deputy_obj.email = row[header['Deputy email']].strip()
        deputy_obj.active = True
        deputy_obj.save()
        obj.deputy_director = deputy_obj
        bp_obj, created = BusinessPartner.objects.get_or_create(name=row[header['BP Name']].strip(),
                                              surname=row[header['BP Surname']].strip())
        bp_obj.bp_email = row[header['BP email']].strip()
        bp_obj.active = True
        bp_obj.save()
        obj.business_partner = bp_obj
        bsce_obj, created = BSCEEmail.objects.get_or_create(bsce_email = row[header['BSCE email']].strip())
        obj.bsce_email = bsce_obj
        obj.save()


import_cc_people_class = ImportInfo({}, 'Cost Centre People',
                                               ['CC Code',
                                                'BP Name', 'BP Surname', 'BP email',
                                                'Deputy Name', 'Deputy Surname', 'Deputy email',
                                                'BSCE email'],
                                            import_cc_responsibles)


def import_director(csvfile):
    """Special function to import Groups with the DG, because I need to change the people
    during the import"""
    reader = csv.reader(csvfile)
    # Convert the first row to a dictionary of positions
    header = csvheadertodict(next(reader))
    for row in reader:
        obj = Directorate.objects.get(
            pk=row[header['Directorate Code']].strip())
        director_obj, created = CostCentrePerson.objects.get_or_create(name=row[header['Director Name']].strip(),
                                              surname=row[header['Director Surname']].strip())
        director_obj.email = row[header['Director email']].strip()
        director_obj.active = True
        director_obj.is_director = True
        director_obj.save()
        obj.director = director_obj
        obj.save()


import_director_class = ImportInfo({}, 'Directors',
                                             ['Directorate Code',
                                              'Directorate Name', 'Directorate Surname',
                                              'Directorate Email'],
                                             import_director)


def import_group_with_dg(csvfile):
    """Special function to import Groups with the DG, because I need to change the people
    during the import"""
    reader = csv.reader(csvfile)
    # Convert the first row to a dictionary of positions
    header = csvheadertodict(next(reader))
    for row in reader:
        obj = DepartmentalGroup.objects.get(
            pk=row[header['Group Code']].strip())
        dg_obj, created = CostCentrePerson.objects.get_or_create(name=row[header['DG Name']].strip(),
                                              surname=row[header['DG Surname']].strip())
        dg_obj.email = row[header['DG email']].strip()
        dg_obj.active = True
        dg_obj.is_dg = True
        dg_obj.save()
        obj.director_general = dg_obj
        obj.save()


import_departmental_group_class = ImportInfo({}, 'Director Generals',
                                               ['Group Code',
                                                'DG Name', 'DG Surname',
                                                'DG email'],
                                               import_group_with_dg)


