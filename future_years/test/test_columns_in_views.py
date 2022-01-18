from django.urls import reverse

from future_years.test.future_year_utils import FutureYearForecastSetup


class ViewFutureForecastColumnTest(FutureYearForecastSetup):
    year_to_date_header = "Year to Date Actuals"
    budget_spent_to_date_header = "budget spent to date"

    def check_response(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "govuk-table")
        self.assertNotContains(response, self.year_to_date_header)
        self.assertNotContains(response, self.budget_spent_to_date_header)

    def test_view_cost_centre_summary(self):
        response = self.client.get(
            reverse(
                "forecast_cost_centre",
                kwargs={
                    "cost_centre_code": self.cost_centre_code,
                    "period": self.future_year,
                },
            ),
        )
        self.check_response(response)


    def test_view_directorate_summary(self):
        response = self.client.get(
            reverse(
                "forecast_directorate",
                kwargs={
                    "directorate_code": self.directorate_code,
                    "period": self.future_year,
                },
            ),
        )
        self.check_response(response)

    def test_view_group_summary(self):
        response = self.client.get(
            reverse(
                "forecast_group",
                kwargs={
                    "group_code": self.group_code,
                    "period": self.future_year,
                },
            )
        )
        self.check_response(response)

    def test_view_dit_summary(self):
        response = self.client.get(
            reverse(
                "forecast_dit",
                kwargs={
                    "period": self.future_year,
                },
            )
        )
        self.check_response(response)

    def test_view_cost_centre_nac_details(self):
        resp = self.client.get(
            reverse(
                "expenditure_details_cost_centre",
                kwargs={
                    "cost_centre_code": self.cost_centre_code,
                    "expenditure_category": self.expenditure_category_id,
                    "budget_type": self.budget_type_id,
                    "period": self.future_year,
                },
            ),
        )
        self.check_response(resp)

    def test_view_directory_nac_details(self):
        resp = self.client.get(
            reverse(
                "expenditure_details_directorate",
                kwargs={
                    "directorate_code": self.directorate_code,
                    "expenditure_category": self.expenditure_category_id,
                    "budget_type": self.budget_type_id,
                    "period": self.future_year,
                },
            ),
        )
        self.check_response(resp)

    def test_view_group_nac_details(self):
        resp = self.client.get(
            reverse(
                "expenditure_details_group",
                kwargs={
                    "group_code": self.group_code,
                    "expenditure_category": self.expenditure_category_id,
                    "budget_type": self.budget_type_id,
                    "period": self.future_year,
                },
            ),
        )

        self.check_response(resp)

    def test_view_dit_nac_details(self):
        resp = self.client.get(
            reverse(
                "expenditure_details_dit",
                kwargs={
                    "expenditure_category": self.expenditure_category_id,
                    "budget_type": self.budget_type_id,
                    "period": self.future_year,
                },
            ),
        )

        self.check_response(resp)

    def test_view_directory_programme_details(self):
        resp = self.client.get(
            reverse(
                "programme_details_directorate",
                kwargs={
                    "directorate_code": self.directorate_code,
                    "programme_code": self.programme_code,
                    "forecast_expenditure_type": self.forecast_expenditure_type_id,
                    "period": self.future_year,
                },
            ),
        )
        self.check_response(resp)

    def test_view_group_programme_details(self):
        resp = self.client.get(
            reverse(
                "programme_details_group",
                kwargs={
                    "group_code": self.group_code,
                    "programme_code": self.programme_code,
                    "forecast_expenditure_type": self.forecast_expenditure_type_id,
                    "period": self.future_year,
                },
            ),
        )

        self.check_response(resp)

    def test_view_dit_programme_details(self):
        resp = self.client.get(
            reverse(
                "programme_details_dit",
                kwargs={
                    "programme_code": self.programme_code,
                    "forecast_expenditure_type": self.forecast_expenditure_type_id,
                    "period": self.future_year,
                },
            ),
        )
        self.check_response(resp)

    def test_view_cost_Centre_project_details(self):
        resp = self.client.get(
            reverse(
                "project_details_costcentre",
                kwargs={
                    "cost_centre_code": self.cost_centre_code,
                    "project_code": self.project_code,
                    "period": self.future_year,
                },
            ),
        )
        self.check_response(resp)

    def test_view_directory_project_details(self):
        resp = self.client.get(
            reverse(
                "project_details_directorate",
                kwargs={
                    "directorate_code": self.directorate_code,
                    "project_code": self.project_code,
                    "period": self.future_year,
                },
            ),
        )
        self.check_response(resp)

    def test_view_group_project_details(self):
        resp = self.client.get(
            reverse(
                "project_details_group",
                kwargs={
                    "group_code": self.group_code,
                    "project_code": self.project_code,
                    "period": self.future_year,
                },
            ),
        )

        self.check_response(resp)

    def test_view_dit_project_details(self):
        resp = self.client.get(
            reverse(
                "project_details_dit",
                kwargs={
                    "project_code": self.project_code,
                    "period": self.future_year,
                },
            ),
        )
        self.check_response(resp)
