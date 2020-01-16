# indicates if DEL, AME, ADMIN
BUDGET_TYPE =  "financial_code__programme__budget_type_fk__budget_type_display"  # noqa
BUDGET_TYPE_ORDER =  "financial_code__programme__budget_type_fk__budget_type_display_order"  # noqa

# Categories defined by DIT: i.e. Consultancy, Contingency, Contractors, etc
BUDGET_CATEGORY_ID = "financial_code__natural_account_code__expenditure_category__id"  # noqa
BUDGET_CATEGORY_NAME = "financial_code__natural_account_code__expenditure_category__grouping_description"   # noqa

# Admin, Capital or Programme
FORECAST_EXPENDITURE_TYPE_CODE = "financial_code__forecast_expenditure_type__forecast_expenditure_type_name"  # noqa
FORECAST_EXPENDITURE_TYPE_ID = "financial_code__forecast_expenditure_type__id"  # noqa
FORECAST_EXPENDITURE_TYPE_NAME = "financial_code__forecast_expenditure_type__forecast_expenditure_type_description"  # noqa
FORECAST_EXPENDITURE_TYPE_ORDER = "financial_code__forecast_expenditure_type__forecast_expenditure_type_display_order"   # noqa

PROGRAMME_CODE = "financial_code__programme__programme_code"
PROGRAMME_NAME = "financial_code__programme__programme_description"

COST_CENTRE_NAME = "financial_code__cost_centre__cost_centre_name"
COST_CENTRE_CODE = "financial_code__cost_centre__cost_centre_code"

DIRECTORATE_NAME = "financial_code__cost_centre__directorate__directorate_name"  # noqa
DIRECTORATE_CODE = "financial_code__cost_centre__directorate__directorate_code"  # noqa

GROUP_NAME = "financial_code__cost_centre__directorate__group__group_name"  # noqa
GROUP_CODE = "financial_code__cost_centre__directorate__group__group_code"  # noqa

NAC_CODE = "financial_code__natural_account_code__natural_account_code"
NAC_NAME = "financial_code__natural_account_code__natural_account_code_description"  # noqa

PROJECT_CODE = "financial_code__project_code__project_code"
PROJECT_NAME = "financial_code__project_code__project_description"

ANALYSIS1_CODE = "financial_code__analysis1_code__analysis1_code"
ANALYSIS1_NAME = "financial_code__analysis1_code__analysis1_description"

ANALYSIS2_CODE = "financial_code__analysis2_code__analysis1_code"
ANALYSIS2_NAME = "financial_code__analysis2_code__analysis1_description"

# PAY, NON-PAY, CAPITAL, NON-CASH
BUDGET_GROUPING = "financial_code__natural_account_code__expenditure_category__NAC_category__NAC_category_description"   # noqa

SHOW_DIT = 0
SHOW_GROUP = 1
SHOW_DIRECTORATE = 2
SHOW_COSTCENTRE = 3


cost_centre_columns = {
    BUDGET_TYPE: "Budget Type",
    COST_CENTRE_NAME: "Cost Centre Description",
    COST_CENTRE_CODE: "Cost Centre Code",
}

directorate_columns = {
    BUDGET_TYPE: "Budget Type",
    DIRECTORATE_NAME: "Directorate Description",
    DIRECTORATE_CODE: "Directorate Code",
}

group_columns = {
    BUDGET_TYPE: "Budget Type",
    GROUP_NAME: "Departmental Group Code",
    GROUP_CODE: "Departmental Group Description",
}
hierarchy_order_list = [BUDGET_TYPE_ORDER]
hierarchy_sub_total = [BUDGET_TYPE]

# programme data
programme_columns = {
    BUDGET_TYPE: "Hidden",
    FORECAST_EXPENDITURE_TYPE_ID: "Hidden",
    FORECAST_EXPENDITURE_TYPE_NAME: "Hidden",
    FORECAST_EXPENDITURE_TYPE_CODE: "Expenditure Type",
    PROGRAMME_NAME: "Programme Description",
    PROGRAMME_CODE: "Programme Code",
}
programme_order_list = [
    BUDGET_TYPE_ORDER,
    FORECAST_EXPENDITURE_TYPE_ORDER,
]
programme_sub_total = [
    BUDGET_TYPE,
    FORECAST_EXPENDITURE_TYPE_NAME,
]
programme_display_sub_total_column = PROGRAMME_NAME

programme_detail_view = [
    'programme_details_dit',
    'programme_details_group',
    'programme_details_directorate',
]


# Expenditure data
expenditure_columns = {
    BUDGET_TYPE: "Hidden",
    BUDGET_CATEGORY_ID: "Hidden",
    BUDGET_GROUPING: "Budget Grouping",
    BUDGET_CATEGORY_NAME: "Budget Category",
}
expenditure_sub_total = [
    BUDGET_TYPE,
    BUDGET_GROUPING,
]
expenditure_display_sub_total_column = BUDGET_CATEGORY_NAME

expenditure_order_list = [
    BUDGET_TYPE_ORDER,
    BUDGET_GROUPING,
]

# Project data
project_columns = {
    BUDGET_TYPE: 'Budget Type',
    PROJECT_NAME: "Project Description",
    PROJECT_CODE: "Project Code",
}
project_order_list = [
    BUDGET_TYPE_ORDER,
]
project_sub_total = [
    BUDGET_TYPE,
]
project_display_sub_total_column = PROJECT_NAME

filter_codes = ['', 'group_code', 'directorate_code', 'cost_centre_code']
filter_selectors = [
    '',
    GROUP_CODE,
    DIRECTORATE_CODE,
    COST_CENTRE_CODE,
]

hierarchy_columns = [
    group_columns,
    directorate_columns,
    cost_centre_columns,
    cost_centre_columns,
]

hierarchy_sub_total_column = [
    GROUP_NAME,
    DIRECTORATE_NAME,
    COST_CENTRE_NAME,
    COST_CENTRE_NAME,
]

expenditure_view = [
    'expenditure_details_dit',
    'expenditure_details_group',
    'expenditure_details_directorate',
    'expenditure_details_cost_centre',
]
# NAC data
nac_columns = {
    BUDGET_CATEGORY_NAME: "Hidden",
    NAC_NAME: "Natural Account Code Description",
    NAC_CODE: "Code",
}
nac_sub_total = [
    BUDGET_CATEGORY_NAME,
]
nac_display_sub_total_column = NAC_NAME

nac_order_list = [
    NAC_NAME,
]

# programme details data
programme_details_dit_columns = {
    PROGRAMME_NAME: "Hidden",
    FORECAST_EXPENDITURE_TYPE_CODE: "Expenditure Type",
    GROUP_NAME: "Departmental Group Code",
    GROUP_CODE: "Departmental Group Description",
}
programme_details_group_columns = {
    PROGRAMME_NAME: "Hidden",
    FORECAST_EXPENDITURE_TYPE_CODE: "Expenditure Type",
    DIRECTORATE_NAME: "Directorate Description",
    DIRECTORATE_CODE: "Directorate Code",
}
programme_details_directorate_columns = {
    PROGRAMME_NAME: "Hidden",
    FORECAST_EXPENDITURE_TYPE_CODE: "Expenditure Type",
    COST_CENTRE_NAME: "Cost Centre Description",
    COST_CENTRE_CODE: "Cost Centre Code",
}
programme_details_sub_total = [
    PROGRAMME_NAME,
]

programme_details_display_sub_total_column = FORECAST_EXPENDITURE_TYPE_CODE

programme_details_dit_order_list = [
    GROUP_NAME,
]
programme_details_group_order_list = [
    DIRECTORATE_NAME,
]
programme_details_directorate_order_list = [
    COST_CENTRE_NAME,
]

programme_details_hierarchy_order_list = [
    programme_details_dit_order_list,
    programme_details_group_order_list,
    programme_details_directorate_order_list,
    '',
]

programme_details_hierarchy_columns = [
    programme_details_dit_columns,
    programme_details_group_columns,
    programme_details_directorate_columns,
    '',
]

programme_details_hierarchy_sub_total_column = [
    GROUP_NAME,
    DIRECTORATE_NAME,
    COST_CENTRE_NAME,
    '',
]

DEFAULT_PIVOT_COLUMNS = {
    COST_CENTRE_CODE: "Cost Centre Code",
    COST_CENTRE_NAME: "Cost Centre Description",
    NAC_CODE: "Natural Account Code",
    NAC_NAME: "Natural Account Code Description",
    PROGRAMME_CODE: "Programme Code",
    PROGRAMME_NAME: "Programme Description",
    ANALYSIS1_CODE: "Contract Code",
    ANALYSIS1_NAME: "Contract Description",
    ANALYSIS2_CODE: "Market Code",
    ANALYSIS2_NAME: "Market Description",
    PROJECT_CODE: "Project Code",
    PROJECT_NAME: "Project Description",
}
