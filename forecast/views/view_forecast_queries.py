# programme__budget_type_fk__budget_type_display
# indicates if DEL, AME, ADMIN used in every view
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

# directorate_filter = {'cost_centre__directorate__directorate_code': '10921F'}
# group_filter = {'cost_centre__directorate__group__group_code': '1090HT'}
# cc_filter = {"cost_centre__cost_centre_code": f"{cost_centre_code}"}
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
    "natural_account_code__expenditure_category__grouping_description": "Budget Category", # noqa
}
