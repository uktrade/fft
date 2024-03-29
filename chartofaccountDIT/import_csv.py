import csv

from chartofaccountDIT.models import (
    Analysis1,
    Analysis2,
    BudgetType,
    CommercialCategory,
    ExpenditureCategory,
    FCOMapping,
    InterEntity,
    InterEntityL1,
    NACCategory,
    NaturalCode,
    OperatingDeliveryCategory,
    ProgrammeCode,
    ProjectCode,
)
from core.import_csv import (
    IMPORT_CSV_FIELDLIST_KEY,
    IMPORT_CSV_IS_FK,
    IMPORT_CSV_MODEL_KEY,
    IMPORT_CSV_PK_KEY,
    IMPORT_CSV_PK_NAME_KEY,
    ImportInfo,
    csv_header_to_dict,
    import_list_obj,
    import_obj,
)
from treasuryCOA.models import L5Account


# define the column position in the csv file.
ANALYSIS1_KEY = {
    IMPORT_CSV_MODEL_KEY: Analysis1,
    IMPORT_CSV_PK_KEY: "Analysis 1 Code",
    IMPORT_CSV_FIELDLIST_KEY: {
        "analysis1_description": "Contract Name",
        "supplier": "Supplier",
        "pc_reference": "PC Reference",
    },
}

ANALYSIS2_KEY = {
    IMPORT_CSV_MODEL_KEY: Analysis2,
    IMPORT_CSV_PK_KEY: "Code",
    IMPORT_CSV_FIELDLIST_KEY: {"analysis2_description": "Description"},
}


def import_analysis1(csvfile):
    return import_obj(csvfile, ANALYSIS1_KEY)


def import_analysis2(csvfile):
    return import_obj(csvfile, ANALYSIS2_KEY)


import_analysis1_class = ImportInfo(ANALYSIS1_KEY)
import_analysis2_class = ImportInfo(ANALYSIS2_KEY)


PROJECT_KEY = {
    IMPORT_CSV_MODEL_KEY: ProjectCode,
    IMPORT_CSV_PK_KEY: "Code",
    IMPORT_CSV_FIELDLIST_KEY: {"project_description": "Description"},
}


def import_Project(csvfile):
    import_obj(csvfile, PROJECT_KEY)


import_project_class = ImportInfo(PROJECT_KEY)

L5_FK_KEY = {
    IMPORT_CSV_MODEL_KEY: L5Account,
    IMPORT_CSV_IS_FK: "",
    IMPORT_CSV_PK_KEY: "L5",
}

OSCAR_FK_KEY = {
    IMPORT_CSV_MODEL_KEY: L5Account,
    IMPORT_CSV_IS_FK: "",
    IMPORT_CSV_PK_KEY: "OSCAR L5 Mapping",
}

NAC_KEY = {
    IMPORT_CSV_MODEL_KEY: NaturalCode,
    IMPORT_CSV_PK_KEY: "L6",
    IMPORT_CSV_FIELDLIST_KEY: {
        "natural_account_code_description": "L6_NAME",
        "economic_budget_code": "DFF-Economic Budget",
        "account_L5_code": L5_FK_KEY,
        "account_L5_code_upload": OSCAR_FK_KEY,
    },
}


def import_nac(csvfile):
    return import_obj(csvfile, NAC_KEY)


def fix_L5_ref():
    """When importing the NAC from
    the flat file provided by BEIS,
    there are references to non
    existing (obsolete) L5 code. If
    there is an alternative L5 code
    in Oscar Upload field, use it.
    This avoids having NAC without a
    budget type (Resource, Capital),
    as it is derived from the L5
    """
    q = NaturalCode.objects.exclude(account_L5_code_upload=None).filter(
        account_L5_code=None
    )
    for r in q:
        r.account_L5_code = r.account_L5_code_upload
        r.save()


import_NAC_class = ImportInfo(NAC_KEY, extra_func=fix_L5_ref)

COMM_CAT_FK_KEY = {
    IMPORT_CSV_MODEL_KEY: CommercialCategory,
    IMPORT_CSV_IS_FK: "",
    IMPORT_CSV_PK_NAME_KEY: "commercial_category",
    IMPORT_CSV_PK_KEY: "Commercial Category",
}

EXP_CAT_FK_KEY = {
    IMPORT_CSV_MODEL_KEY: ExpenditureCategory,
    IMPORT_CSV_IS_FK: "",
    IMPORT_CSV_PK_NAME_KEY: "grouping_description",
    IMPORT_CSV_PK_KEY: "Budget Category",
}

NAC_DIT_KEY = {
    IMPORT_CSV_MODEL_KEY: NaturalCode,
    IMPORT_CSV_PK_KEY: "NAC",
    IMPORT_CSV_FIELDLIST_KEY: {
        "active": "Active",
        "commercial_category": COMM_CAT_FK_KEY,
        "expenditure_category": EXP_CAT_FK_KEY,
    },
}  # noqa: E501


def import_nac_dit_specific_fields(csvfile):
    return import_obj(csvfile, NAC_DIT_KEY)


import_NAC_DIT_class = ImportInfo(NAC_DIT_KEY)

NAC_CATEGORY_KEY = {
    IMPORT_CSV_MODEL_KEY: NACCategory,
    IMPORT_CSV_PK_KEY: "Budget Grouping",
    IMPORT_CSV_PK_NAME_KEY: "NAC_category_description",
    IMPORT_CSV_FIELDLIST_KEY: {},
}


def import_nac_expenditure_category(csvfile):
    return import_obj(csvfile, NAC_CATEGORY_KEY)


import_NAC_category_class = ImportInfo(NAC_CATEGORY_KEY)

OP_DEL_CATEGORY_KEY = {
    IMPORT_CSV_MODEL_KEY: OperatingDeliveryCategory,
    IMPORT_CSV_PK_KEY: "Operating Delivery Category",
    IMPORT_CSV_PK_NAME_KEY: "operating_delivery_description",
    IMPORT_CSV_FIELDLIST_KEY: {},
}

import_op_del_category_class = ImportInfo(OP_DEL_CATEGORY_KEY)


def import_expenditure_category(csvfile):
    """Special function to import Expenditure
    category, because I need to change the
    NAC code during the import"""
    reader = csv.reader(csvfile)
    # Convert the first row to a dictionary of positions
    header = csv_header_to_dict(next(reader))
    for row in reader:
        obj, created = ExpenditureCategory.objects.get_or_create(
            grouping_description=row[header["budget category"]].strip()
        )
        nac_obj = NaturalCode.objects.get(pk=row[header["budget nac"]].strip())
        nac_obj.active = True
        nac_obj.used_for_budget = True
        nac_obj.save()
        obj.linked_budget_code = nac_obj
        obj.description = row[header["description"]].strip()
        obj.further_description = row[header["further description"]].strip()
        cat_obj = NACCategory.objects.get(
            NAC_category_description=row[header["budget grouping"]].strip()
        )
        obj.NAC_category = cat_obj
        op_plan_obj, created = OperatingDeliveryCategory.objects.get_or_create(
            operating_delivery_description=row[
                header["operating delivery plan"]
            ].strip()
        )
        obj.op_del_category = op_plan_obj
        obj.save()
    return True, ""


import_expenditure_category_class = ImportInfo(
    {},
    "Budget Categories",
    [
        "Budget Grouping",
        "Budget Category",
        "Description",
        "Further description",
        "Budget NAC",
        "Operating Delivery Plan",
    ],
    special_import_func=import_expenditure_category,
)


def import_nac_category(csvfile):
    return import_list_obj(csvfile, NACCategory, "NAC_category_description")


COMMERCIAL_CATEGORY_KEY = {
    IMPORT_CSV_MODEL_KEY: CommercialCategory,
    IMPORT_CSV_PK_KEY: "Commercial Category",
    IMPORT_CSV_PK_NAME_KEY: "commercial_category",
    IMPORT_CSV_FIELDLIST_KEY: {
        "description": "Description",
        "approvers": "Approvers",
    },
}


def import_commercial_category(csvfile):
    return import_obj(csvfile, COMMERCIAL_CATEGORY_KEY)


import_comm_cat_class = ImportInfo(COMMERCIAL_CATEGORY_KEY)

BUDGET_KEY = {
    IMPORT_CSV_MODEL_KEY: BudgetType,
    IMPORT_CSV_PK_KEY: "type",
    IMPORT_CSV_IS_FK: "",
    IMPORT_CSV_PK_NAME_KEY: "budget_type",
}

PROG_KEY = {
    IMPORT_CSV_MODEL_KEY: ProgrammeCode,
    IMPORT_CSV_PK_KEY: "Code",
    IMPORT_CSV_FIELDLIST_KEY: {
        "programme_description": "Description",
        "budget_type": BUDGET_KEY,
    },
}


def import_programme(csvfile):
    return import_obj(csvfile, PROG_KEY)


import_prog_class = ImportInfo(PROG_KEY)

INTER_ENTITY_L1_KEY = {
    IMPORT_CSV_MODEL_KEY: InterEntityL1,
    IMPORT_CSV_PK_KEY: "L1 Value",
    IMPORT_CSV_FIELDLIST_KEY: {"l1_description": "L1 Description"},
}

INTER_ENTITY_KEY = {
    IMPORT_CSV_MODEL_KEY: InterEntity,
    IMPORT_CSV_PK_KEY: "L2 Value",
    IMPORT_CSV_FIELDLIST_KEY: {
        "l1_description": "L2 Description",
        "cpid": "CPID",
        "active": "Enable",
        "l1_value": INTER_ENTITY_L1_KEY,
    },
}


def import_inter_entity(csvfile):
    import_obj(csvfile, INTER_ENTITY_KEY)


import_inter_entity_class = ImportInfo(INTER_ENTITY_KEY)

L6_KEY = {
    IMPORT_CSV_MODEL_KEY: NaturalCode,
    IMPORT_CSV_IS_FK: "",
    IMPORT_CSV_PK_KEY: "ORACLE Code",
}

FCO_MAPPING_KEY = {
    IMPORT_CSV_MODEL_KEY: FCOMapping,
    IMPORT_CSV_PK_KEY: "FCO Code",
    IMPORT_CSV_FIELDLIST_KEY: {
        "fco_description": "FCO Description",
        "account_L6_code_fk": L6_KEY,
    },
}

import_fco_mapping_class = ImportInfo(FCO_MAPPING_KEY)
