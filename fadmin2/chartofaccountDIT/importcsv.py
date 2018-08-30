from .models import Analysis1, Analysis2, NaturalCode, \
    ExpenditureCategory, NACCategory, CommercialCategory, \
    ProgrammeCode
from treasuryCOA.models import L5Account
from core.myutils import import_obj, import_list_obj, \
    IMPORT_CSV_MODEL_KEY, IMPORT_CSV_PK_KEY, IMPORT_CSV_FIELDLIST_KEY, \
    IMPORT_CSV_IS_FK

import csv

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


L5_FK_KEY = {IMPORT_CSV_MODEL_KEY: L5Account,
             IMPORT_CSV_IS_FK: '',
             IMPORT_CSV_PK_KEY: 'OSCAR L5 Mapping'
             }

NAC_KEY = {IMPORT_CSV_MODEL_KEY: NaturalCode,
           IMPORT_CSV_PK_KEY: 'L6',
           IMPORT_CSV_FIELDLIST_KEY: {NaturalCode.natural_account_code_description.field_name: 'L6_NAME',  # noqa: E501
                                      NaturalCode.account_L5_code.field.name: L5_FK_KEY}}


# /Users/stronal/Downloads/dbfiles/4.Account Codes.csv
# csvfile = open(path, newline='', encoding='cp1252')

def import_NAC(csvfile):
    import_obj(csvfile, NAC_KEY)


def import_NAC_expenditure_category(csvfile):
    import_list_obj(csvfile, ExpenditureCategory, 'grouping_description')


def import_NAC_dashboard_Budget(csvfile):
    reader = csv.reader(csvfile)
    next(reader)  # skip the header
    for row in reader:
        obj = ExpenditureCategory.objects.get(grouping_description=row[0].strip())
        print(row[0].strip())
        nac_obj = NaturalCode.objects.get(pk=row[1].strip())
        nac_obj.active = True
        nac_obj.used_for_budget = True
        nac_obj.save()
        obj.linked_budget_code = nac_obj
        obj.save()


def import_expenditure_category(csvfile):
    reader = csv.reader(csvfile)
    next(reader)  # skip the header
    for row in reader:
        print(row[1].strip())
        obj = ExpenditureCategory.objects.get(grouping_description=row[1].strip())
        obj.description = row[2].strip()
        obj.further_description = row[3].strip()
        cat_obj = NACCategory.objects.get(NAC_category_description=row[0].strip())
        obj.NAC_category = cat_obj
        obj.save()


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
