# monthly_figure__financial_code__programme__budget_type_fk__budget_type_display
# indicates if DEL, AME, ADMIN
# It is used in every view
cost_centre_columns = {
    "monthly_figure__financial_code__programme__budget_type_fk__budget_type_display": "Budget Type",
    "monthly_figure__financial_code__cost_centre__cost_centre_name": "Cost Centre Description",
    "monthly_figure__financial_code__cost_centre__cost_centre_code": "Cost Centre Code",
}

directorate_columns = {
    "monthly_figure__financial_code__programme__budget_type_fk__budget_type_display": "Budget Type",
    "monthly_figure__financial_code__cost_centre__directorate__directorate_name": "Directorate Description",
    "monthly_figure__financial_code__cost_centre__directorate__directorate_code": "Directorate Code",
}

group_columns = {
    "monthly_figure__financial_code__programme__budget_type_fk__budget_type_display": "Budget Type",
    "monthly_figure__financial_code__cost_centre__directorate__group__group_code": "Departmental Group Description",
    "monthly_figure__financial_code__cost_centre__directorate__group__group_name": "Departmental Group Code",
}
hierarchy_order_list = ["monthly_figure__financial_code__programme__budget_type_fk__budget_type_display_order"]
hierarchy_sub_total = ["monthly_figure__financial_code__programme__budget_type_fk__budget_type_display"]

# programme data
programme_columns = {
    "monthly_figure__financial_code__programme__budget_type_fk__budget_type_display": "Hidden",
    "monthly_figure__financial_code__forecast_expenditure_type__forecast_expenditure_type_description": "Hidden",
    "monthly_figure__financial_code__forecast_expenditure_type__forecast_expenditure_type_name": "Expenditure Type",
    "monthly_figure__financial_code__programme__programme_description": "Programme Description",
    "monthly_figure__financial_code__programme__programme_code": "Programme Code",
}
programme_order_list = [
    "monthly_figure__financial_code__programme__budget_type_fk__budget_type_display_order",
    "monthly_figure__financial_code__forecast_expenditure_type__forecast_expenditure_type_display_order",
]
programme_sub_total = [
    "monthly_figure__financial_code__programme__budget_type_fk__budget_type_display",
    "monthly_figure__financial_code__forecast_expenditure_type__forecast_expenditure_type_description",
]
programme_display_sub_total_column = "monthly_figure__financial_code__programme__programme_description"

# Expenditure data
expenditure_columns = {
    "monthly_figure__financial_code__programme__budget_type_fk__budget_type_display": "Hidden",
    "monthly_figure__financial_code__natural_account_code__expenditure_category__NAC_category__NAC_category_description": "Budget Grouping",  # noqa
    "monthly_figure__financial_code__natural_account_code__expenditure_category__grouping_description":
        "Budget Category",
}
expenditure_sub_total = [
    "monthly_figure__financial_code__programme__budget_type_fk__budget_type_display",
    "monthly_figure__financial_code__natural_account_code__expenditure_category__NAC_category__NAC_category_description",  # noqa
]
expenditure_display_sub_total_column = (
    "monthly_figure__financial_code__natural_account_code__expenditure_category__grouping_description"
)
expenditure_order_list = [
    "monthly_figure__financial_code__programme__budget_type_fk__budget_type_display_order",
    "monthly_figure__financial_code__natural_account_code__expenditure_category__NAC_category__NAC_category_description",  # noqa
]

# Project data
project_columns = {
    "monthly_figure__financial_code__programme__budget_type_fk__budget_type_display": 'Budget Type',
    "monthly_figure__financial_code__project_code__project_description": "Project Description",
    "monthly_figure__financial_code__project_code__project_code": "Project Code",
}
project_order_list = [
    "monthly_figure__financial_code__programme__budget_type_fk__budget_type_display_order",
]
project_sub_total = [
    "monthly_figure__financial_code__programme__budget_type_fk__budget_type_display",
]
project_display_sub_total_column = "monthly_figure__financial_code__project_code__project_description"

SHOW_DIT = 0
SHOW_GROUP = 1
SHOW_DIRECTORATE = 2
SHOW_COSTCENTRE = 3

filter_codes = ['', 'group_code', 'directorate_code', 'cost_centre_code']
filter_selectors = [
    '',
    'monthly_figure__financial_code__cost_centre__directorate__group__group_code',
    'monthly_figure__financial_code__cost_centre__directorate__directorate_code',
    'monthly_figure__financial_code__cost_centre__cost_centre_code',
]

hierarchy_columns = [
    group_columns,
    directorate_columns,
    cost_centre_columns,
    cost_centre_columns,
]

hierarchy_sub_total_column = [
    'monthly_figure__financial_code__cost_centre__directorate__group__group_code',
    'monthly_figure__financial_code__cost_centre__directorate__directorate_name',
    'monthly_figure__financial_code__cost_centre__cost_centre_name',
    'monthly_figure__financial_code__cost_centre__cost_centre_name',
]
