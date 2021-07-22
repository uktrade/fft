from forecast.utils.query_fields import ForecastQueryFields


class FigureFieldData:

    select_related_list = [
        "financial_code",
        "financial_code__cost_centre",
        "financial_code__natural_account_code",
        "financial_code__programme",
        "financial_code__project_code",
        "financial_code__analysis1_code",
        "financial_code__analysis2_code",
        "financial_code__forecast_expenditure_type",
    ]
    chart_of_account_titles = [
        "Cost Centre code",
        "Actual NAC",
        "Programme code",
        "Contract code",
        "Market code",
        "Project code",
        "Expenditure type",
        "Expenditure type description",
    ]

    def set_fields(self):
        # Define the access strings for the chart of account members needed
        # for actuals, forecasts and budgets figures
        self.fields = ForecastQueryFields()
        self.cost_centre_field = self.fields.cost_centre_code_field
        self.nac_field = self.fields.nac_code_field
        self.programme_field = self.fields.programme_code_field
        self.contract_field = self.fields.analysis1_code_field
        self.market_field = self.fields.analysis2_code_field
        self.project_field = self.fields.project_code_field
        self.expenditure_type_field = self.fields.expenditure_type_name_field
        self.expenditure_type_description_field = (
            self.fields.expenditure_type_description_field
        )

        self.chart_of_account_field_list = [
            self.cost_centre_field,
            self.nac_field,
            self.programme_field,
            self.contract_field,
            self.market_field,
            self.project_field,
            self.expenditure_type_field,
            self.expenditure_type_description_field,
        ]
