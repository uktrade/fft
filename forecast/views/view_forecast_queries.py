# programme__budget_type_fk__budget_type_display
# indicates if DEL, AME, ADMIN
# It is used in every view
cost_centre_columns = {
    "programme__budget_type_fk__budget_type_display": "Budget Type",
    "cost_centre__cost_centre_name": "Cost Centre Description",
    "cost_centre__cost_centre_code": "Cost Centre Code",
}

directorate_columns = {
    "programme__budget_type_fk__budget_type_display": "Budget Type",
    "cost_centre__directorate__directorate_name": "Directorate Description",
    "cost_centre__directorate__directorate_code": "Directorate Code",
}

group_columns = {
    "programme__budget_type_fk__budget_type_display": "Budget Type",
    "cost_centre__directorate__group__group_code": "Departmental Group Description",
    "cost_centre__directorate__group__group_name": "Departmental Group Code",
}
hierarchy_order_list = ["programme__budget_type_fk__budget_type_display_order"]
hierarchy_sub_total = ["programme__budget_type_fk__budget_type_display"]

# programme data
programme_columns = {
    "programme__budget_type_fk__budget_type_display": "Hidden",
    "forecast_expenditure_type__forecast_expenditure_type_description": "Hidden",
    "forecast_expenditure_type__forecast_expenditure_type_name": "Expenditure Type",
    "programme__programme_description": "Programme Description",
    "programme__programme_code": "Programme Code",
}
programme_order_list = [
    "programme__budget_type_fk__budget_type_display_order",
    "forecast_expenditure_type__forecast_expenditure_type_display_order",
]
programme_sub_total = [
    "programme__budget_type_fk__budget_type_display",
    "forecast_expenditure_type__forecast_expenditure_type_description",
]
programme_display_sub_total_column = "programme__programme_description"

# Expenditure data
expenditure_columns = {
    "programme__budget_type_fk__budget_type_display": "Hidden",
    "natural_account_code__expenditure_category__NAC_category__NAC_category_description": "Budget Grouping",  # noqa
    "natural_account_code__expenditure_category__grouping_description":
        "Budget Category",
}
expenditure_sub_total = [
    "programme__budget_type_fk__budget_type_display",
    "natural_account_code__expenditure_category__NAC_category__NAC_category_description",  # noqa
]
expenditure_display_sub_total_column = (
    "natural_account_code__expenditure_category__grouping_description"
)
expenditure_order_list = [
    "programme__budget_type_fk__budget_type_display_order",
    "natural_account_code__expenditure_category__NAC_category__NAC_category_description",  # noqa
]

# Project data
project_columns = {
    "programme__budget_type_fk__budget_type_display": 'Budget Type',
    "project_code__project_description": "Project Description",
    "project_code__project_code": "Project Code",
}
project_order_list = [
    "programme__budget_type_fk__budget_type_display_order",
]
project_sub_total = [
    "programme__budget_type_fk__budget_type_display",
]
project_display_sub_total_column = "project_code__project_description"

SHOW_DIT = 0
SHOW_GROUP = 1
SHOW_DIRECTORATE = 2
SHOW_COSTCENTRE = 3

filter_codes = ['', 'group_code', 'directorate_code', 'cost_centre_code']
filter_selectors = [
    '',
    'cost_centre__directorate__group__group_code',
    'cost_centre__directorate__directorate_code',
    'cost_centre__cost_centre_code',
]

hierarchy_columns = [
    group_columns,
    directorate_columns,
    cost_centre_columns,
    cost_centre_columns,
]

hierarchy_sub_total_column = [
    'cost_centre__directorate__group__group_code',
    'cost_centre__directorate__directorate_name',
    'cost_centre__cost_centre_name',
    'cost_centre__cost_centre_name',
]
