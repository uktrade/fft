import csv

from core.myutils import IMPORT_CSV_FIELDLIST_KEY, IMPORT_CSV_IS_FK, IMPORT_CSV_MODEL_KEY, \
    IMPORT_CSV_PK_KEY, IMPORT_CSV_PK_NAME_KEY, csvheadertodict, import_list_obj, \
    import_obj, ImportInfo

from treasuryCOA.models import L5Account

from .models import Analysis1, Analysis2, CommercialCategory, ExpenditureCategory, \
    NACCategory, NaturalCode, ProgrammeCode


# define the column position in the csv file.
ANALYSIS1_KEY = {IMPORT_CSV_MODEL_KEY: Analysis1,
                 IMPORT_CSV_PK_KEY: 'Code',
                 IMPORT_CSV_FIELDLIST_KEY: {Analysis1.analysis1_description.field_name: 'Description'}}  # noqa: E501

ANALYSIS2_KEY = {IMPORT_CSV_MODEL_KEY: Analysis2,
                 IMPORT_CSV_PK_KEY: 'Code',
                 IMPORT_CSV_FIELDLIST_KEY: {Analysis2.analysis2_description.field_name: 'Description'}}  # noqa: E501


def import_Analysis1(csvfile):
    import_obj(csvfile, ANALYSIS1_KEY)


def import_Analysis2(csvfile):
    import_obj(csvfile, ANALYSIS2_KEY)


import_a1_class = ImportInfo(ANALYSIS1_KEY)
import_a2_class = ImportInfo(ANALYSIS2_KEY)


L5_FK_KEY = {IMPORT_CSV_MODEL_KEY: L5Account,
             IMPORT_CSV_IS_FK: '',
             IMPORT_CSV_PK_KEY: 'OSCAR L5 Mapping'
             }

NAC_KEY = {IMPORT_CSV_MODEL_KEY: NaturalCode,
           IMPORT_CSV_PK_KEY: 'L6',
           IMPORT_CSV_FIELDLIST_KEY: {NaturalCode.natural_account_code_description.field_name: 'L6_NAME',  # noqa: E501
                                      NaturalCode.account_L5_code.field.name: L5_FK_KEY}}


def import_NAC(csvfile):
    import_obj(csvfile, NAC_KEY)


import_NAC_class = ImportInfo(NAC_KEY)


NAC_CATEGORY_KEY = {IMPORT_CSV_MODEL_KEY: NACCategory,
                    IMPORT_CSV_PK_KEY: 'Budget Grouping',
                    IMPORT_CSV_PK_NAME_KEY: NACCategory.NAC_category_description.field_name,
                    IMPORT_CSV_FIELDLIST_KEY: {}}


def import_NAC_expenditure_category(csvfile):
    import_obj(csvfile, NAC_CATEGORY_KEY)


import_NAC_category_class = ImportInfo(NAC_CATEGORY_KEY)


def import_expenditure_category(csvfile):
    reader = csv.reader(csvfile)
    # Convert the first row to a dictionary of positions
    header = csvheadertodict(next(reader))
    row_number = 1
    for row in reader:
        import pdb;
        pdb.set_trace()
        obj, created = ExpenditureCategory.objects.get_or_create(grouping_description=row[header['Expenditure Category']].strip())
        nac_obj = NaturalCode.objects.get(pk=row[header['Budget NAC']].strip())
        nac_obj.active = True
        nac_obj.used_for_budget = True
        nac_obj.save()
        obj.linked_budget_code = nac_obj
        obj.description = row[header['Description']].strip()
        obj.further_description = row[header['Further Information']].strip()
        cat_obj = NACCategory.objects.get(NAC_category_description=row[header['Budget Grouping']].strip())
        obj.NAC_category = cat_obj
        obj.save()


import_expenditure_category_class = ImportInfo({},'Expenditure Categories',
                                               ['Budget Grouping','Expenditure Category','Description','Further Information','Budget NAC'], import_expenditure_category)


def import_NAC_category(csvfile):
    import_list_obj(csvfile, NACCategory, 'NAC_category_description')


def import_NAC_DIT_setting(csvfile):
    reader = csv.reader(csvfile)
    next(reader)  # skip the header
    linenum = 1
    for row in reader:
        linenum = linenum + 1
        nac_obj = NaturalCode.objects.get(pk=row[0].strip())
        nac_obj.expenditure_category = \
            ExpenditureCategory.objects.get(grouping_description=row[2].strip())
        nac_obj.active = True
        nac_obj.save()


def import_NAC_DIT_budget(csvfile):
    reader = csv.reader(csvfile)
    next(reader)  # skip the header
    linenum = 1
    for row in reader:
        linenum = linenum + 1
        nac_obj = NaturalCode.objects.get(pk=row[1].strip())
        nac_obj.active = True
        nac_obj.save()


def import_commercial_category(csvfile):
    import_list_obj(csvfile, CommercialCategory, 'commercial_category')


def import_commercial_category_responsible(csvfile):
    reader = csv.reader(csvfile)
    next(reader)  # skip the header
    linenum = 1
    for row in reader:
        linenum = linenum + 1
        obj = CommercialCategory.objects.get(commercial_category=row[0].strip())
        obj.approvers = row[2].strip()
        obj.save()


PROG_KEY = {IMPORT_CSV_MODEL_KEY: ProgrammeCode,
            IMPORT_CSV_PK_KEY: 'Code',
            IMPORT_CSV_FIELDLIST_KEY: {ProgrammeCode.programme_description.field_name: 'Description',  # noqa: E501
                                       ProgrammeCode.budget_type.field_name: 'Type'}}


def import_programme(csvfile):
    import_obj(csvfile, PROG_KEY)


import_prog_class = ImportInfo(PROG_KEY)
