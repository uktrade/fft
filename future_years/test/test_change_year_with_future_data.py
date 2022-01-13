from forecast.test.test_new_financial_year_command import NewFinancialYearTest


class NewFinancialYearWithFutureYearDataTest(NewFinancialYearTest):
    def setUp(self):
        super().setUp()
        self.init_data.set_year(self.current_year + 1)
        self.init_data.setup_forecast()
        self.init_data.setup_budget()

        self.init_data.set_year(self.current_year + 2)
        self.init_data.setup_forecast()
        self.init_data.setup_budget()
        self.init_data.set_year(self.current_year)
