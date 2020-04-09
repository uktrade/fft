from core.import_csv import (
    IMPORT_CSV_FIELDLIST_KEY,
    IMPORT_CSV_MODEL_KEY,
    IMPORT_CSV_PK_KEY,
    ImportInfo,
    import_obj,
)

from .models import L1Account, L2Account, L3Account, L4Account, L5Account

# define the column position in the csv file.
# The following is the list of headers in the structure report downloaded Treasury
# COLUMN_KEY = {
#     'Accounts Code': 0,
#     'Accounts Long Name': 1,
#     'Account L0 Code': 2,
#     'Account L0 Long Name': 3,
#     'Account L1 Code': 4,
#     'Account L1 Long Name': 5,
#     'Account L2 Code': 6,
#     'Account L2 Long Name': 7,
#     'Account L3 Code': 8,
#     'Account L3 Long Name': 9,
#     'Account L4 Code': 10,
#     'Account L4 Long Name': 11,
#     'Account L5 Code': 12,
#     'Account L5 Long Name': 13,
#     'Account L5 Description': 14,
#     'Economic Category Code': 15,
#     'Economic Category Long Name': 16,
#     'Economic Group Code': 17,
#     'Economic Group Long Name': 18,
#     'Economic Ringfence Code': 19,
#     'Economic Ringfence Long Name': 20,
#     'Economic Budget Code': 21,
#     'PESA Economic Group Code': 22,
#     'Sector Code': 23,
#     'TES Code': 24,
#     'ESA Code': 25,
#     'ESA Long Name': 26,
#     'ESA Group Code': 27,
#     'ESA Group Long Name': 28,
#     'PSAT Code': 29,
#     'PSAT Long Name': 30,
#     'National Accounts Code': 31,
#     'National Accounts Long Name': 32,
#     'Estimates Sub-Category Code': 33,
#     'Estimates Category Code': 34,
#     'Income Category Code': 35,
#     'Estimates Column Code': 36,
#     'Usage Code': 37,
#     'Cash Indicator Code': 38
# }

# noqa: E501 tells Flake8 to ignore lines that are to long
L1_KEY = {
    IMPORT_CSV_MODEL_KEY: L1Account,
    IMPORT_CSV_PK_KEY: "Account L1 Code",
    IMPORT_CSV_FIELDLIST_KEY: {
        L1Account.account_l1_long_name.field_name: "Account L1 Long Name",  # noqa: E501
        L1Account.account_code.field_name: "Accounts Code",
        L1Account.account_l0_code.field_name: "Account L0 Code",
    },
}

L2_KEY = {
    IMPORT_CSV_MODEL_KEY: L2Account,
    IMPORT_CSV_PK_KEY: "Account L2 Code",
    IMPORT_CSV_FIELDLIST_KEY: {
        L2Account.account_l2_long_name.field_name: "Account L2 Long Name",  # noqa: E501
        L2Account.account_l1.field.name: L1_KEY,
    },
}

L3_KEY = {
    IMPORT_CSV_MODEL_KEY: L3Account,
    IMPORT_CSV_PK_KEY: "Account L3 Code",
    IMPORT_CSV_FIELDLIST_KEY: {
        L3Account.account_l3_long_name.field_name: "Account L3 Long Name",  # noqa: E501
        L3Account.account_l2.field.name: L2_KEY,
    },
}

L4_KEY = {
    IMPORT_CSV_MODEL_KEY: L4Account,
    IMPORT_CSV_PK_KEY: "Account L4 Code",
    IMPORT_CSV_FIELDLIST_KEY: {
        L4Account.account_l4_long_name.field_name: "Account L4 Long Name",  # noqa: E501
        L4Account.account_l3.field.name: L3_KEY,
    },
}

L5_KEY = {
    IMPORT_CSV_MODEL_KEY: L5Account,
    IMPORT_CSV_PK_KEY: "Account L5 Code",
    IMPORT_CSV_FIELDLIST_KEY: {
        L5Account.account_l5_long_name.field_name: "Account L5 Long Name",  # noqa: E501
        L5Account.account_l5_description.field_name: "Account L5 Description",
        # noqa: E501
        L5Account.economic_budget_code.field_name: "Economic Budget Code",  # noqa: E501
        L5Account.sector_code.field_name: "Sector Code",
        L5Account.estimates_column_code.field_name: "Estimates Column Code",  # noqa: E501
        L5Account.usage_code.field_name: "Usage Code",
        L5Account.cash_indicator_code.field_name: "Cash Indicator Code",  # noqa: E501
        L5Account.account_l4.field.name: L4_KEY,
    },
}


def import_treasury_COA(csvfile):
    import_obj(csvfile, L5_KEY)


import_L5_class = ImportInfo(L5_KEY, "Treasury Chart of Account")
