import csv

from core.importcsv import IMPORT_CSV_FIELDLIST_KEY, IMPORT_CSV_IS_FK, IMPORT_CSV_MODEL_KEY, \
    IMPORT_CSV_PK_KEY, IMPORT_CSV_PK_NAME_KEY, ImportInfo, csvheadertodict, \
    import_list_obj, import_obj

from treasuryCOA.models import L5Account

from .models import Analysis1, Analysis2, BudgetType, CommercialCategory, ExpenditureCategory, FCOMapping, \
    InterEntity, InterEntityL1, NACCategory, NaturalCode, OperatingDeliveryCategory, ProgrammeCode, ProjectCode

# define the column position in the csv file.
ANALYSIS1_KEY = {IMPORT_CSV_MODEL_KEY: Analysis1,
                 IMPORT_CSV_PK_KEY: 'Analysis 1 Code',
                 IMPORT_CSV_FIELDLIST_KEY: {
                     Analysis1.analysis1_description.field_name: 'Contract Name',
                     Analysis1.supplier.field_name: 'Supplier',
                     Analysis1.pc_reference.field_name: 'PC Reference',
                 }}  # noqa: E501

ANALYSIS2_KEY = {IMPORT_CSV_MODEL_KEY: Analysis2,
                 IMPORT_CSV_PK_KEY: 'Code',
                 IMPORT_CSV_FIELDLIST_KEY: {
                     Analysis2.analysis2_description.field_name: 'Description',
                 }}


def import_Analysis1(csvfile):
    import_obj(csvfile, ANALYSIS1_KEY)


def import_Analysis2(csvfile):
    import_obj(csvfile, ANALYSIS2_KEY)


import_a1_class = ImportInfo(ANALYSIS1_KEY)
import_a2_class = ImportInfo(ANALYSIS2_KEY)

PROJECT_KEY = {IMPORT_CSV_MODEL_KEY: ProjectCode,
               IMPORT_CSV_PK_KEY: 'Code',
               IMPORT_CSV_FIELDLIST_KEY: {
                   ProjectCode.project_description.field_name: 'Description',
               }}


def import_Project(csvfile):
    import_obj(csvfile, PROJECT_KEY)


import_project_class = ImportInfo(PROJECT_KEY)

L5_FK_KEY = {IMPORT_CSV_MODEL_KEY: L5Account,
             IMPORT_CSV_IS_FK: '',
             IMPORT_CSV_PK_KEY: 'L5'
             }

OSCAR_FK_KEY = {IMPORT_CSV_MODEL_KEY: L5Account,
                IMPORT_CSV_IS_FK: '',
                IMPORT_CSV_PK_KEY: 'OSCAR L5 Mapping'
                }

NAC_KEY = {IMPORT_CSV_MODEL_KEY: NaturalCode,
           IMPORT_CSV_PK_KEY: 'L6',
           IMPORT_CSV_FIELDLIST_KEY: {
               NaturalCode.natural_account_code_description.field_name: 'L6_NAME',  # noqa: E501
               NaturalCode.account_L5_code.field.name: L5_FK_KEY,
               NaturalCode.account_L5_code_upload.field.name: OSCAR_FK_KEY,
           }}


def import_NAC(csvfile):
    import_obj(csvfile, NAC_KEY)


def fix_L5_ref():
    """When importing the NAC from the flat file provided by BEIS, there are references to non existing (obsolete)
     L5 code. If there is an alternative L5 code in Oscar Upload field, use it. This avoids having NAC without a
     budget type (Resource, Capital), as it is derived from the L5
    """
    q = NaturalCode.objects.exclude(account_L5_code_upload=None).filter(account_L5_code=None)
    for r in q:
        print(r.account_L5_code)
        r.account_L5_code = r.account_L5_code_upload
        r.save()


import_NAC_class = ImportInfo(NAC_KEY, extra_func=fix_L5_ref)

COMM_CAT_FK_KEY = {IMPORT_CSV_MODEL_KEY: CommercialCategory,
                   IMPORT_CSV_IS_FK: '',
                   IMPORT_CSV_PK_NAME_KEY: CommercialCategory.commercial_category.field_name,
                   IMPORT_CSV_PK_KEY: 'Commercial Category'
                   }

EXP_CAT_FK_KEY = {IMPORT_CSV_MODEL_KEY: ExpenditureCategory,
                  IMPORT_CSV_IS_FK: '',
                  IMPORT_CSV_PK_NAME_KEY: ExpenditureCategory.grouping_description.field_name,
                  IMPORT_CSV_PK_KEY: 'Budget Category'
                  }

NAC_DIT_KEY = {IMPORT_CSV_MODEL_KEY: NaturalCode,
               IMPORT_CSV_PK_KEY: 'NAC',
               IMPORT_CSV_FIELDLIST_KEY: {NaturalCode.active.field_name: 'Active',
                                          NaturalCode.commercial_category.field.name: COMM_CAT_FK_KEY,  # noqa: E501
                                          NaturalCode.expenditure_category.field.name: EXP_CAT_FK_KEY}}  # noqa: E501


def import_NAC_DIT(csvfile):
    import_obj(csvfile, NAC_DIT_KEY)


import_NAC_DIT_class = ImportInfo(NAC_DIT_KEY)

NAC_CATEGORY_KEY = {IMPORT_CSV_MODEL_KEY: NACCategory,
                    IMPORT_CSV_PK_KEY: 'Budget Grouping',
                    IMPORT_CSV_PK_NAME_KEY: NACCategory.NAC_category_description.field_name,
                    IMPORT_CSV_FIELDLIST_KEY: {}}


def import_NAC_expenditure_category(csvfile):
    import_obj(csvfile, NAC_CATEGORY_KEY)


import_NAC_category_class = ImportInfo(NAC_CATEGORY_KEY)

OP_DEL_CATEGORY_KEY = {IMPORT_CSV_MODEL_KEY: OperatingDeliveryCategory,
                       IMPORT_CSV_PK_KEY: 'Operating Delivery Category',
                       IMPORT_CSV_PK_NAME_KEY: OperatingDeliveryCategory.operating_delivery_description.field_name,
                       IMPORT_CSV_FIELDLIST_KEY: {}}

import_op_del_category_class = ImportInfo(OP_DEL_CATEGORY_KEY)


def import_expenditure_category(csvfile):
    """Special function to import Expenditure category, because I need to change the NAC code
    during the import"""
    reader = csv.reader(csvfile)
    # Convert the first row to a dictionary of positions
    header = csvheadertodict(next(reader))
    for row in reader:
        obj, created = ExpenditureCategory.objects.get_or_create(
            grouping_description=row[header['budget category']].strip())
        nac_obj = NaturalCode.objects.get(pk=row[header['budget nac']].strip())
        nac_obj.active = True
        nac_obj.used_for_budget = True
        nac_obj.save()
        obj.linked_budget_code = nac_obj
        obj.description = row[header['description']].strip()
        obj.further_description = row[header['further description']].strip()
        cat_obj = NACCategory.objects.get(
            NAC_category_description=row[header['budget grouping']].strip())
        obj.NAC_category = cat_obj
        op_plan_obj, created = OperatingDeliveryCategory.objects.get_or_create(
            operating_delivery_description=row[header['operating delivery plan']].strip())
        obj.op_del_category = op_plan_obj
        obj.save()


import_expenditure_category_class = ImportInfo({}, 'Budget Categories',
                                               ['Budget Grouping', 'Budget Category',
                                                'Description', 'Further description',
                                                'Budget NAC', 'Operating Delivery Plan'],
                                               my_import_func=import_expenditure_category)


def import_NAC_category(csvfile):
    import_list_obj(csvfile, NACCategory, 'NAC_category_description')


COMMERCIAL_CATEGORY_KEY = {IMPORT_CSV_MODEL_KEY: CommercialCategory,
                           IMPORT_CSV_PK_KEY: 'Commercial Category',
                           IMPORT_CSV_PK_NAME_KEY: CommercialCategory.commercial_category.field_name,  # noqa: E501
                           IMPORT_CSV_FIELDLIST_KEY:
                               {CommercialCategory.description.field_name: 'Description',
                                CommercialCategory.approvers.field_name: 'Approvers'}}


def import_commercial_category(csvfile):
    import_obj(csvfile, COMMERCIAL_CATEGORY_KEY)


import_comm_cat_class = ImportInfo(COMMERCIAL_CATEGORY_KEY)

BUDGET_KEY = {IMPORT_CSV_MODEL_KEY: BudgetType,
              IMPORT_CSV_PK_KEY: 'type',
              IMPORT_CSV_IS_FK: '',
              IMPORT_CSV_PK_NAME_KEY: BudgetType.budget_type.field_name
              }

PROG_KEY = {IMPORT_CSV_MODEL_KEY: ProgrammeCode,
            IMPORT_CSV_PK_KEY: 'Code',
            IMPORT_CSV_FIELDLIST_KEY: {
                ProgrammeCode.programme_description.field_name: 'Description',  # noqa: E501
                ProgrammeCode.budget_type_fk.field.name: BUDGET_KEY}}


def import_programme(csvfile):
    import_obj(csvfile, PROG_KEY)


import_prog_class = ImportInfo(PROG_KEY)

INTER_ENTITY_L1_KEY = {IMPORT_CSV_MODEL_KEY: InterEntityL1,
                       IMPORT_CSV_PK_KEY: 'L1 Value',
                       IMPORT_CSV_FIELDLIST_KEY: {
                           InterEntityL1.l1_description.field_name: 'L1 Description'}}

INTER_ENTITY_KEY = {IMPORT_CSV_MODEL_KEY: InterEntity,
                    IMPORT_CSV_PK_KEY: 'L2 Value',
                    IMPORT_CSV_FIELDLIST_KEY: {
                        InterEntity.l2_description.field_name: 'L2 Description',
                        InterEntity.cpid.field_name: 'CPID',
                        InterEntity.active.field_name: 'Enable',
                        InterEntity.l1_value.field.name: INTER_ENTITY_L1_KEY
                    }}


def import_inter_entity(csvfile):
    import_obj(csvfile, INTER_ENTITY_KEY)


import_inter_entity_class = ImportInfo(INTER_ENTITY_KEY)

L6_KEY = {IMPORT_CSV_MODEL_KEY: NaturalCode,
          IMPORT_CSV_IS_FK: '',
          IMPORT_CSV_PK_KEY: 'ORACLE Code'
          }

FCO_MAPPING_KEY = {IMPORT_CSV_MODEL_KEY: FCOMapping,
                   IMPORT_CSV_PK_KEY: 'FCO Code',
                   IMPORT_CSV_FIELDLIST_KEY: {
                       FCOMapping.fco_description.field_name: 'FCO Description',
                       FCOMapping.account_L6_code_fk.field.name: L6_KEY
                   }
                   }

import_fco_mapping_class = ImportInfo(FCO_MAPPING_KEY)
