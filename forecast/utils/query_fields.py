financial_code_prefix = "financial_code__"
# indicates if DEL, AME, ADMIN
BUDGET_TYPE =  f"{financial_code_prefix}programme__budget_type_fk__budget_type_display"  # noqa
BUDGET_TYPE_ORDER =  f"{financial_code_prefix}programme__budget_type_fk__budget_type_display_order"  # noqa
BUDGET_TYPE_EDIT_ORDER =  f"{financial_code_prefix}programme__budget_type_fk__budget_type_edit_display_order"  # noqa

# Categories defined by DIT: i.e. Consultancy, Contingency, Contractors, etc
BUDGET_CATEGORY_ID = f"{financial_code_prefix}natural_account_code__expenditure_category__id"  # noqa
BUDGET_CATEGORY_NAME = f"{financial_code_prefix}natural_account_code__expenditure_category__grouping_description"   # noqa

# PAY, NON-PAY, CAPITAL, NON-CASH
BUDGET_GROUPING = f"{financial_code_prefix}natural_account_code__expenditure_category__NAC_category__NAC_category_description"   # noqa
BUDGET_GROUPING_ORDERING = f"{financial_code_prefix}natural_account_code__expenditure_category__NAC_category__NAC_category_display_order"   # noqa
BUDGET_NAC_CODE = f"{financial_code_prefix}natural_account_code__expenditure_category__linked_budget_code"  # noqa
BUDGET_NAC_CODE_DESCRIPTION = f"{financial_code_prefix}natural_account_code__expenditure_category__linked_budget_code__natural_account_code_description"  # noqa

# Admin, Capital or Programme
FORECAST_EXPENDITURE_TYPE_NAME = f"{financial_code_prefix}forecast_expenditure_type__forecast_expenditure_type_name"  # noqa
FORECAST_EXPENDITURE_TYPE_DESCRIPTION = f"{financial_code_prefix}forecast_expenditure_type__forecast_expenditure_type_description"  # noqa
FORECAST_EXPENDITURE_TYPE_ORDER = f"{financial_code_prefix}forecast_expenditure_type__forecast_expenditure_type_display_order"   # noqa

PROGRAMME_CODE = f"{financial_code_prefix}programme__programme_code"
PROGRAMME_NAME = f"{financial_code_prefix}programme__programme_description"

COST_CENTRE_NAME = f"{financial_code_prefix}cost_centre__cost_centre_name"
COST_CENTRE_CODE = f"{financial_code_prefix}cost_centre__cost_centre_code"

DIRECTORATE_NAME = f"{financial_code_prefix}cost_centre__directorate__directorate_name"  # noqa
DIRECTORATE_CODE = f"{financial_code_prefix}cost_centre__directorate__directorate_code"  # noqa

GROUP_NAME = f"{financial_code_prefix}cost_centre__directorate__group__group_name"  # noqa
GROUP_CODE = f"{financial_code_prefix}cost_centre__directorate__group__group_code"  # noqa

NAC_CODE = f"{financial_code_prefix}natural_account_code__natural_account_code"
NAC_NAME = f"{financial_code_prefix}natural_account_code__natural_account_code_description"  # noqa
NAC_EXPENDITURE_TYPE = f"{financial_code_prefix}natural_account_code__economic_budget_code"  # noqa


PROJECT_CODE = f"{financial_code_prefix}project_code__project_code"
PROJECT_NAME = f"{financial_code_prefix}project_code__project_description"

ANALYSIS1_CODE = f"{financial_code_prefix}analysis1_code__analysis1_code"
ANALYSIS1_NAME = f"{financial_code_prefix}analysis1_code__analysis1_description"

ANALYSIS2_CODE = f"{financial_code_prefix}analysis2_code__analysis2_code"
ANALYSIS2_NAME = f"{financial_code_prefix}analysis2_code__analysis2_description"

SHOW_DIT = 0
SHOW_GROUP = 1
SHOW_DIRECTORATE = 2
SHOW_COSTCENTRE = 3


cost_centre_columns = {
    BUDGET_TYPE: "Budget type",
    COST_CENTRE_NAME: "Cost Centre description",
    COST_CENTRE_CODE: "code",
}

directorate_columns = {
    BUDGET_TYPE: "Budget Type",
    DIRECTORATE_NAME: "Directorate description",
    DIRECTORATE_CODE: "code",
}

group_columns = {
    BUDGET_TYPE: "Budget Type",
    GROUP_NAME: "Departmental Group description",
    GROUP_CODE: "code",
}
hierarchy_order_list = [BUDGET_TYPE_ORDER]
hierarchy_sub_total = [BUDGET_TYPE]

# programme data
programme_columns = {
    BUDGET_TYPE: "Hidden",
    FORECAST_EXPENDITURE_TYPE_DESCRIPTION: "Hidden",
    FORECAST_EXPENDITURE_TYPE_NAME: "Expenditure type",
    PROGRAMME_NAME: "Programme code",
    PROGRAMME_CODE: "code",
}

programme_order_list = [
    BUDGET_TYPE_ORDER,
    FORECAST_EXPENDITURE_TYPE_ORDER,
]
programme_sub_total = [
    BUDGET_TYPE,
    FORECAST_EXPENDITURE_TYPE_DESCRIPTION,
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
    BUDGET_GROUPING: "Budget grouping",
    BUDGET_CATEGORY_NAME: "Budget category",
}
expenditure_sub_total = [
    BUDGET_TYPE,
    BUDGET_GROUPING,
]
expenditure_display_sub_total_column = BUDGET_CATEGORY_NAME

expenditure_order_list = [
    BUDGET_TYPE_ORDER,
    BUDGET_GROUPING_ORDERING,
]

# Project data
project_columns = {
    PROJECT_NAME: "Project",
    PROJECT_CODE: "code",
    FORECAST_EXPENDITURE_TYPE_ORDER: "Hidden",
    FORECAST_EXPENDITURE_TYPE_NAME: "Expenditure type",
}
project_order_list = [
    PROJECT_CODE,
    FORECAST_EXPENDITURE_TYPE_ORDER,
]
project_sub_total = [
    PROJECT_NAME,
]
project_display_sub_total_column = PROJECT_CODE

project_detail_view = [
    'project_details_dit',
    'project_details_group',
    'project_details_directorate',
    'project_details_costcentre',
]

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

hierarchy_view_link_column = [
    GROUP_NAME,
    DIRECTORATE_NAME,
    COST_CENTRE_NAME,
]

hierarchy_view = [
    'forecast_group',
    'forecast_directorate',
    'forecast_cost_centre'
]

hierarchy_view_code = [
    GROUP_CODE,
    DIRECTORATE_CODE,
    COST_CENTRE_CODE,
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
    NAC_NAME: "Natural Account code",
    NAC_CODE: "code",
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
    FORECAST_EXPENDITURE_TYPE_NAME: "Expenditure type",
    GROUP_NAME: "Departmental Group",
    GROUP_CODE: "code",
}
programme_details_group_columns = {
    PROGRAMME_NAME: "Hidden",
    FORECAST_EXPENDITURE_TYPE_NAME: "Expenditure type",
    DIRECTORATE_NAME: "Directorate",
    DIRECTORATE_CODE: "code",
}

programme_details_directorate_columns = {
    PROGRAMME_NAME: "Hidden",
    FORECAST_EXPENDITURE_TYPE_NAME: "Expenditure type",
    COST_CENTRE_NAME: "Cost Centre",
    COST_CENTRE_CODE: "code",
}

programme_details_sub_total = [
    PROGRAMME_NAME,
]

programme_details_display_sub_total_column = FORECAST_EXPENDITURE_TYPE_NAME

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


# Project details views
project_details_dit_columns = {
    FORECAST_EXPENDITURE_TYPE_NAME: "Expenditure type",
    GROUP_NAME: "Departmental Group",
    GROUP_CODE: "code",
}
project_details_group_columns = {
    FORECAST_EXPENDITURE_TYPE_NAME: "Expenditure type",
    DIRECTORATE_NAME: "Directorate",
    DIRECTORATE_CODE: "code",
}
project_details_directorate_columns = {
    FORECAST_EXPENDITURE_TYPE_NAME: "Expenditure type",
    COST_CENTRE_NAME: "Cost Centre",
    COST_CENTRE_CODE: "code",
}
project_details_costcentre_columns = {
    FORECAST_EXPENDITURE_TYPE_NAME: "Expenditure type",
    COST_CENTRE_NAME: "Cost Centre",
    COST_CENTRE_CODE: "code",
}

project_details_sub_total = [
    FORECAST_EXPENDITURE_TYPE_NAME,
]

project_details_dit_order_list = [
    GROUP_NAME,
    FORECAST_EXPENDITURE_TYPE_NAME,
]
project_details_group_order_list = [
    DIRECTORATE_NAME,
    FORECAST_EXPENDITURE_TYPE_NAME,
]
project_details_directorate_order_list = [
    COST_CENTRE_NAME,
    FORECAST_EXPENDITURE_TYPE_NAME,
]

project_details_costcentre_order_list = [
    FORECAST_EXPENDITURE_TYPE_NAME,
]

project_details_hierarchy_order_list = [
    project_details_dit_order_list,
    project_details_group_order_list,
    project_details_directorate_order_list,
    project_details_costcentre_order_list,
]

project_details_hierarchy_columns = [
    project_details_dit_columns,
    project_details_group_columns,
    project_details_directorate_columns,
    project_details_costcentre_columns,
]

project_details_hierarchy_sub_total_column = [
    GROUP_NAME,
    DIRECTORATE_NAME,
    COST_CENTRE_NAME,
    COST_CENTRE_NAME,
]


DEFAULT_PIVOT_COLUMNS = {
    COST_CENTRE_CODE: "Cost Centre code",
    COST_CENTRE_NAME: "Cost Centre description",
    NAC_CODE: "Natural Account code",
    NAC_NAME: "Natural Account code description",
    PROGRAMME_CODE: "Programme code",
    PROGRAMME_NAME: "Programme code description",
    ANALYSIS1_CODE: "Contract code",
    ANALYSIS1_NAME: "Contract description",
    ANALYSIS2_CODE: "Market code",
    ANALYSIS2_NAME: "Market description",
    PROJECT_CODE: "Project code",
    PROJECT_NAME: "Project description",
}


VIEW_FORECAST_DOWNLOAD_COLUMNS = {
    GROUP_NAME: "Group name",
    GROUP_CODE: "Group code",
    DIRECTORATE_NAME: "Directorate name",
    DIRECTORATE_CODE: "Directorate code",
    COST_CENTRE_NAME: "Cost Centre name",
    COST_CENTRE_CODE: "Cost Centre code",
    BUDGET_GROUPING: "Budget grouping",
    FORECAST_EXPENDITURE_TYPE_NAME: "Expenditure type",
    FORECAST_EXPENDITURE_TYPE_DESCRIPTION: "Expenditure type description",
    BUDGET_TYPE: "Budget Type",
    BUDGET_CATEGORY_NAME: "Budget category",
    BUDGET_NAC_CODE: "Budget/Forecast NAC",
    BUDGET_NAC_CODE_DESCRIPTION: "Budget/Forecast NAC description",
    NAC_CODE: "PO/Actual NAC",
    NAC_NAME: "Natural Account code description",
    NAC_EXPENDITURE_TYPE: "NAC Expenditure type",
    PROGRAMME_CODE: "Programme code",
    PROGRAMME_NAME: "Programme code description",
    ANALYSIS1_CODE: "Contract code",
    ANALYSIS1_NAME: "Contract description",
    ANALYSIS2_CODE: "Market code",
    ANALYSIS2_NAME: "Market description",
    PROJECT_CODE: "Project code",
    PROJECT_NAME: "Project description",
}


EDIT_KEYS_DOWNLOAD = {
    PROGRAMME_CODE: 'Programme code',
    PROGRAMME_NAME: "Programme code Description",
    NAC_CODE: 'Natural Account code',
    NAC_NAME: "Natural Account Code Description",
    ANALYSIS1_CODE: 'Contract Code',
    ANALYSIS2_CODE: 'Market Code',
    PROJECT_CODE: 'Project Code',
}


EDIT_FORECAST_DOWNLOAD_COLUMNS = {
    GROUP_NAME: "Group name",
    GROUP_CODE: "Group code",
    DIRECTORATE_NAME: "Directorate name",
    DIRECTORATE_CODE: "Directorate code",
    COST_CENTRE_NAME: "Cost Centre name",
    COST_CENTRE_CODE: "Cost Centre code",
    BUDGET_GROUPING: "Budget Grouping",
    FORECAST_EXPENDITURE_TYPE_NAME: "Expenditure type",
    FORECAST_EXPENDITURE_TYPE_DESCRIPTION: "Expenditure type description",
    BUDGET_TYPE: "Budget type",
    BUDGET_CATEGORY_NAME: "Budget Category",
    BUDGET_NAC_CODE: "Budget/Forecast NAC",
    BUDGET_NAC_CODE_DESCRIPTION: "Budget/Forecast NAC Description",
    NAC_EXPENDITURE_TYPE: "NAC Expenditure Type",
    ANALYSIS1_NAME: "Contract Description",
    ANALYSIS2_NAME: "Market Description",
    PROJECT_NAME: "Project Description",
}

EDIT_FORECAST_DOWNLOAD_ORDER = [
    BUDGET_TYPE_EDIT_ORDER,
    PROGRAMME_CODE,
    BUDGET_GROUPING_ORDERING,
    NAC_CODE,
]


def edit_forecast_order():
    # remove financial_code__ prefix from the
    # fields used in the download order.
    order_list = []
    prefix_len = len(financial_code_prefix)
    for elem in EDIT_FORECAST_DOWNLOAD_ORDER:
        order_list.append(elem[prefix_len:])
    return order_list


MI_REPORT_DOWNLOAD_COLUMNS = {
    COST_CENTRE_CODE: "Cost Centre code",
    NAC_CODE: 'Natural Account code',
    PROGRAMME_CODE: 'Programme code',
    ANALYSIS1_CODE: 'Contract Code',
    ANALYSIS2_CODE: 'Market Code',
    PROJECT_CODE: 'Project Code',
}
