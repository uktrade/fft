# programme__budget_type_fk__budget_type_display
# indicates if DEL, AME, ADMIN
# It is used in every view
budget_type_cost_centre_columns = {
    "programme__budget_type_fk__budget_type_display": "Budget_type",
    "cost_centre__cost_centre_name": "Cost Centre Description",
    "cost_centre__cost_centre_code": "Cost Centre Code",
}

budget_type_cost_directorate_columns = {
    "programme__budget_type_fk__budget_type_display": "Budget_type",
    "cost_centre__directorate__directorate_name": "Directorate Description",
    "cost_centre__directorate__directorate_code": "Directorate Code",
}

budget_type_cost_group_columns = {
    "programme__budget_type_fk__budget_type_display": "Budget_type",
    "cost_centre__directorate__group__group_code": "Departmental Group Description",
    "cost_centre__directorate__group__group_name": "Departmental Group Code",
}

programme_columns = {
    "programme__budget_type_fk__budget_type_display": "Hidden",
    "forecast_expenditure_type__forecast_expenditure_type_description": "Hidden",
    "forecast_expenditure_type__forecast_expenditure_type_name": "Expenditure Type",
    "programme__programme_description": "Programme Description",
    "programme__programme_code": "Programme Code",
}

natural_account_columns = {
    "programme__budget_type_fk__budget_type_display": "Hidden",
    "natural_account_code__expenditure_category__NAC_category__NAC_category_description": "Budget Grouping", # noqa
    "natural_account_code__expenditure_category__grouping_description":
        "Budget Category",
}

order_list_hierarchy = ["programme__budget_type_fk__budget_type_display_order"]

sub_total_hierarchy = ["programme__budget_type_fk__budget_type_display"]
display_sub_total_column_cost_centre = "cost_centre__cost_centre_name"

# programme data
order_list_prog = [
    "programme__budget_type_fk__budget_type_display_order",
    "forecast_expenditure_type__forecast_expenditure_type_display_order",
]
sub_total_prog = [
    "programme__budget_type_fk__budget_type_display",
    "forecast_expenditure_type__forecast_expenditure_type_description",
]
display_sub_total_column_prog = "programme__programme_description"

# NAC data
sub_total_nac = [
    "programme__budget_type_fk__budget_type_display",
    "natural_account_code__expenditure_category__NAC_category__NAC_category_description", # noqa
]
display_sub_total_column_nac = (
    "natural_account_code__expenditure_category__grouping_description"
)
order_list_nac = [
    "programme__budget_type_fk__budget_type_display_order",
    "natural_account_code__expenditure_category__NAC_category__NAC_category_description", # noqa
]

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


hierarchy_query = [
    budget_type_cost_group_columns,
    budget_type_cost_directorate_columns,
    budget_type_cost_centre_columns,
    budget_type_cost_centre_columns,
]

hierarchy_sub_total_column = [
    'cost_centre__directorate__group__group_code',
    'cost_centre__directorate__directorate_name',
    'cost_centre__cost_centre_name',
    'cost_centre__cost_centre_name',
]
