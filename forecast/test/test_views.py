from bs4 import BeautifulSoup


from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    Permission,
)
from django.urls import reverse

from chartofaccountDIT.test.factories import (
    ExpenditureCategoryFactory,
    NaturalCodeFactory,
    ProgrammeCodeFactory,
    ProjectCodeFactory,
)

from core.models import FinancialYear
from core.test.test_base import TEST_EMAIL, BaseTestCase
from core.utils.generic_helpers import get_current_financial_year

from costcentre.test.factories import (
    CostCentreFactory,
    DepartmentalGroupFactory,
    DirectorateFactory,
)

from forecast.models import (
    FinancialCode,
    FinancialPeriod,
    ForecastEditState,
    ForecastMonthlyFigure,
)
from forecast.permission_shortcuts import assign_perm
from forecast.test.factories import (
    FinancialCodeFactory,
)

from forecast.test.test_utils import (
    TOTAL_COLUMN,
    SPEND_TO_DATE_COLUMN,
    UNDERSPEND_COLUMN,
    create_budget,
    format_forecast_figure,
)


class ViewPermissionsTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)
        self.test_cost_centre = 888812
        self.cost_centre_code = self.test_cost_centre
        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )

    def test_edit_forecast_view_permission(self):
        edit_forecast_url = reverse(
            "edit_forecast",
            kwargs={
                'cost_centre_code': self.cost_centre_code,
            }
        )

        resp = self.client.get(
            edit_forecast_url,
        )

        assert resp.status_code == 302
        assert resp.url == reverse(
            "forecast_cost_centre",
            kwargs={
                "cost_centre_code": self.cost_centre_code,
                "period": 0,
            }
        )

    def test_edit_forecast_view(self):
        # Add forecast view permission
        can_view_forecasts = Permission.objects.get(
            codename='can_view_forecasts'
        )
        self.test_user.user_permissions.add(can_view_forecasts)
        self.test_user.save()

        self.assertFalse(
            self.test_user.has_perm(
                "change_costcentre",
                self.cost_centre,
            )
        )

        edit_forecast_url = reverse(
            "edit_forecast",
            kwargs={
                'cost_centre_code': self.cost_centre_code
            }
        )

        resp = self.client.get(
            edit_forecast_url,
        )

        # Should have been redirected (no permission)
        self.assertEqual(resp.status_code, 302)

        assign_perm("change_costcentre", self.test_user, self.cost_centre)

        self.assertTrue(self.test_user.has_perm("change_costcentre", self.cost_centre))

        resp = self.client.get(
            edit_forecast_url,
        )

        # Should be allowed
        self.assertEqual(resp.status_code, 200)


class AddForecastRowTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)
        self.nac_code = 999999
        self.cost_centre_code = 888812
        self.analysis_1_code = "1111111"
        self.analysis_2_code = "2222222"
        self.project_code = "3000"

        self.programme = ProgrammeCodeFactory.create()
        self.nac = NaturalCodeFactory.create(natural_account_code=self.nac_code)
        self.project = ProjectCodeFactory.create(project_code=self.project_code)
        self.analysis_1 = Analysis1Factory.create(analysis1_code=self.analysis_1_code)
        self.analysis_2 = Analysis2Factory.create(analysis2_code=self.analysis_2_code)
        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )

    def add_row_get_response(self, url):
        return self.client.get(url)

    def add_row_post_response(self, url, post_content):
        return self.client.post(
            url,
            data=post_content,
        )

    def edit_row_get_response(self):
        edit_view_url = reverse(
            "edit_forecast",
            kwargs={
                'cost_centre_code': self.cost_centre_code
            },
        )

        return self.client.get(edit_view_url)

    def test_view_add_row(self):
        assign_perm("change_costcentre", self.test_user, self.cost_centre)

        assert FinancialCode.objects.count() == 0

        add_resp = self.add_row_get_response(
            reverse(
                "add_forecast_row",
                kwargs={
                    'cost_centre_code': self.cost_centre_code
                },
            ),
        )

        self.assertEqual(add_resp.status_code, 200)

        # add_forecast_row
        add_row_resp = self.add_row_post_response(
            reverse(
                "add_forecast_row",
                kwargs={
                    'cost_centre_code': self.cost_centre_code
                },
            ),
            {
                "programme": self.programme.programme_code,
                "natural_account_code": self.nac.natural_account_code,
            },
        )

        self.assertEqual(add_row_resp.status_code, 302)

        assert FinancialCode.objects.count() == 1

    def test_view_add_row_with_period_actual(self):
        assign_perm("change_costcentre", self.test_user, self.cost_centre)

        # financial period with actual
        financial_period = FinancialPeriod.objects.get(
            financial_period_code=1,
        )
        financial_period.actual_loaded = True
        financial_period.save()

        assert ForecastMonthlyFigure.objects.count() == 0

        # add_forecast_row
        add_row_resp = self.add_row_post_response(
            reverse(
                "add_forecast_row",
                kwargs={
                    'cost_centre_code': self.cost_centre_code
                },
            ),
            {
                "programme": self.programme.programme_code,
                "natural_account_code": self.nac.natural_account_code,
            },
        )

        self.assertEqual(add_row_resp.status_code, 302)

        assert ForecastMonthlyFigure.objects.count() == 1

        monthly_figure = ForecastMonthlyFigure.objects.first()

        assert monthly_figure.financial_period.financial_period_code == financial_period.financial_period_code  # noqa

    def test_duplicate_values_invalid(self):
        assign_perm("change_costcentre", self.test_user, self.cost_centre)

        # add forecast row
        response = self.add_row_post_response(
            reverse(
                "add_forecast_row",
                kwargs={
                    'cost_centre_code': self.cost_centre_code
                },
            ),
            {
                "programme": self.programme.programme_code,
                "natural_account_code": self.nac.natural_account_code,
                "analysis1_code": self.analysis_1_code,
                "analysis2_code": self.analysis_2_code,
                "project_code": self.project_code,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(FinancialCode.objects.count(), 1)

        response_2 = self.add_row_post_response(
            reverse(
                "add_forecast_row",
                kwargs={
                    'cost_centre_code': self.cost_centre_code
                },
            ),
            {
                "programme": self.programme.programme_code,
                "natural_account_code": self.nac.natural_account_code,
                "analysis1_code": self.analysis_1_code,
                "analysis2_code": self.analysis_2_code,
                "project_code": self.project_code,
            },
        )

        self.assertEqual(response_2.status_code, 200)

        assert "govuk-list govuk-error-summary__list" in str(
            response_2.rendered_content,
        )
        self.assertEqual(FinancialCode.objects.count(), 1)

    def test_duplicate_values_different_cost_centre_valid(self):
        cost_centre_code_2 = self.cost_centre_code + 1

        cost_centre_2 = CostCentreFactory.create(
            cost_centre_code=cost_centre_code_2,
        )

        assign_perm("change_costcentre", self.test_user, self.cost_centre)
        assign_perm("change_costcentre", self.test_user, cost_centre_2)

        # add forecast row
        response = self.add_row_post_response(
            reverse(
                "add_forecast_row",
                kwargs={
                    'cost_centre_code': self.cost_centre_code
                },
            ),
            {
                "programme": self.programme.programme_code,
                "natural_account_code": self.nac.natural_account_code,
                "analysis1_code": self.analysis_1_code,
                "analysis2_code": self.analysis_2_code,
                "project_code": self.project_code,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(FinancialCode.objects.count(), 1)

        response_2 = self.add_row_post_response(
            reverse(
                "add_forecast_row",
                kwargs={
                    'cost_centre_code': cost_centre_code_2,
                },
            ),
            {
                "programme": self.programme.programme_code,
                "natural_account_code": self.nac.natural_account_code,
                "analysis1_code": self.analysis_1_code,
                "analysis2_code": self.analysis_2_code,
                "project_code": self.project_code,
            },
        )

        self.assertEqual(response_2.status_code, 302)
        self.assertEqual(FinancialCode.objects.count(), 2)


class ChooseCostCentreTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)

        self.cost_centre_code = 109076
        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )

    def test_choose_cost_centre(self):
        assign_perm("change_costcentre", self.test_user, self.cost_centre)

        response = self.client.get(
            reverse(
                "choose_cost_centre"
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        response = self.client.post(
            reverse(
                "choose_cost_centre"
            ),
            data={
                "cost_centre": self.cost_centre_code
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        # Check we've been forwarded to edit page
        assert "/forecast/edit/" in response.url

    def test_cost_centre_json(self):
        assign_perm("change_costcentre", self.test_user, self.cost_centre)

        response = self.client.get(
            reverse(
                "choose_cost_centre"
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            f'window.costCentres = [{{"name": "{self.cost_centre.cost_centre_name}", "code": "{self.cost_centre_code}"}}];'  # noqa E501
        )

    def test_finance_admin_cost_centre_access(self):
        finance_admins = Group.objects.get(
            name='Finance Administrator',
        )
        finance_admins.user_set.add(self.test_user)
        finance_admins.save()

        # Bust permissions cache (refresh_from_db does not work)
        self.test_user, _ = get_user_model().objects.get_or_create(
            email=self.test_user.email
        )

        # Check that no cost centres can be accessed
        response = self.client.get(
            reverse(
                "choose_cost_centre"
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_finance_business_partner_cost_centre_access(self):
        finance_business_partners = Group.objects.get(
            name='Finance Business Partner/BSCE',
        )
        finance_business_partners.user_set.add(self.test_user)
        finance_business_partners.save()

        # Bust permissions cache (refresh_from_db does not work)
        self.test_user, _ = get_user_model().objects.get_or_create(
            email=self.test_user.email
        )

        # Check that no cost centres can be accessed
        response = self.client.get(
            reverse(
                "choose_cost_centre"
            )
        )
        assert response.status_code == 403

        assign_perm("change_costcentre", self.test_user, self.cost_centre)

        response = self.client.get(
            reverse(
                "choose_cost_centre"
            ),
        )

        self.assertEqual(
            response.status_code,
            200,
        )



class ViewForecastNaturalAccountCodeTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)
        self.group_name = "Test Group"
        self.group_code = "TestGG"
        self.directorate_name = "Test Directorate"
        self.directorate_code = "TestDD"
        self.cost_centre_code = 109076

        self.group = DepartmentalGroupFactory(
            group_code=self.group_code,
            group_name=self.group_name,
        )
        self.directorate = DirectorateFactory(
            directorate_code=self.directorate_code,
            directorate_name=self.directorate_name,
            group=self.group,
        )
        self.cost_centre = CostCentreFactory(
            directorate=self.directorate,
            cost_centre_code=self.cost_centre_code,
        )
        current_year = get_current_financial_year()
        self.amount1_apr = -9876543
        self.amount2_apr = 1000000

        programme_obj = ProgrammeCodeFactory()
        self.budget_type = programme_obj.budget_type.budget_type_display
        expenditure_obj = ExpenditureCategoryFactory()
        self.expenditure_id = expenditure_obj.id
        self.nac1_obj = NaturalCodeFactory(natural_account_code=12345678,
                                           expenditure_category=expenditure_obj
                                           )
        self.nac2_obj = NaturalCodeFactory(expenditure_category=expenditure_obj)
        year_obj = FinancialYear.objects.get(financial_year=current_year)

        apr_period = FinancialPeriod.objects.get(financial_period_code=1)
        apr_period.actual_loaded = True
        apr_period.save()

        # If you use the MonthlyFigureFactory the test fails.
        # I cannot work out why, it may be due to using a random year....
        financial_code1_obj = FinancialCode.objects.create(
            programme=programme_obj,
            cost_centre=self.cost_centre,
            natural_account_code=self.nac1_obj,
        )
        financial_code1_obj.save
        financial_code2_obj = FinancialCode.objects.create(
            programme=programme_obj,
            cost_centre=self.cost_centre,
            natural_account_code=self.nac2_obj,
        )
        financial_code2_obj.save
        apr_figure = ForecastMonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=1
            ),
            financial_code=financial_code1_obj,
            financial_year=year_obj,
            amount=self.amount1_apr,
        )
        apr_figure.save

        apr_figure = ForecastMonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=1
            ),
            financial_code=financial_code2_obj,
            financial_year=year_obj,
            amount=self.amount2_apr
        )
        apr_figure.save

        self.amount_may = 1234567
        may_figure = ForecastMonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=4
            ),
            financial_code=financial_code1_obj,
            financial_year=year_obj,
            amount=self.amount_may
        )
        may_figure.save

        # Assign forecast view permission
        can_view_forecasts = Permission.objects.get(
            codename='can_view_forecasts'
        )
        self.test_user.user_permissions.add(can_view_forecasts)
        self.test_user.save()

        # Bust permissions cache (refresh_from_db does not work)
        self.test_user, _ = get_user_model().objects.get_or_create(
            email=TEST_EMAIL
        )

        self.budget = create_budget(financial_code2_obj, year_obj)
        self.year_total = self.amount1_apr + self.amount2_apr + self.amount_may
        self.underspend_total = \
            self.budget - self.amount1_apr - self.amount_may - self.amount2_apr
        self.spend_to_date_total = self.amount1_apr + self.amount2_apr

    def check_nac_table(self, table):
        nac_rows = table.find_all("tr")
        first_nac_cols = nac_rows[2].find_all("td")
        assert (
            first_nac_cols[0].get_text().strip() == self.nac2_obj.natural_account_code_description  # noqa
        )

        assert first_nac_cols[3].get_text().strip() == format_forecast_figure(
            self.budget / 100
        )

        last_nac_cols = nac_rows[-1].find_all("td")
        # Check the total for the year
        assert last_nac_cols[TOTAL_COLUMN].get_text().strip() == \
            format_forecast_figure(self.year_total / 100)
        # Check the difference between budget and year total
        assert last_nac_cols[UNDERSPEND_COLUMN].get_text().strip() == \
            format_forecast_figure(self.underspend_total / 100)
        # Check the spend to date
        assert last_nac_cols[SPEND_TO_DATE_COLUMN].get_text().strip() == \
            format_forecast_figure(self.spend_to_date_total / 100)

    def check_negative_value_formatted(self, soup, lenght):
        negative_values = soup.find_all("span", class_="negative")
        assert len(negative_values) == lenght

    def check_response(self, resp):
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "govuk-table")

        soup = BeautifulSoup(resp.content, features="html.parser")

        # Check that there is 1 table
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 1

        # Check that all the subtotal hierachy_rows exist
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 4

        self.check_negative_value_formatted(soup, 6)

        # Check that the only table displays the nac and the correct totals
        self.check_nac_table(tables[0])

    def test_view_cost_centre_nac_details(self):
        resp = self.client.get(
            reverse(
                "expenditure_details_cost_centre",
                kwargs={
                    'cost_centre_code': self.cost_centre_code,
                    'expenditure_category': self.expenditure_id,
                    'budget_type': self.budget_type,
                    'period': 0,
                },
            ),
        )
        self.check_response(resp)

    def test_view_directory_nac_details(self):
        resp = self.client.get(
            reverse(
                "expenditure_details_directorate",
                kwargs={
                    'directorate_code': self.directorate.directorate_code,
                    'expenditure_category': self.expenditure_id,
                    'budget_type': self.budget_type,
                    'period': 0,
                },
            ),
        )
        self.check_response(resp)

    def test_view_group_nac_details(self):
        resp = self.client.get(
            reverse(
                "expenditure_details_group",
                kwargs={
                    'group_code': self.group.group_code,
                    'expenditure_category': self.expenditure_id,
                    'budget_type': self.budget_type,
                    'period': 0,
                },
            )
        )

        self.check_response(resp)

    def test_view_dit_nac_details(self):
        resp = self.client.get(
            reverse(
                "expenditure_details_dit",
                kwargs={
                    'expenditure_category': self.expenditure_id,
                    'budget_type': self.budget_type,
                    'period': 0,
                },
            )
        )

        self.check_response(resp)


class ViewProgrammeDetailsTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)

        self.group_name = "Test Group"
        self.group_code = "TestGG"
        self.directorate_name = "Test Directorate"
        self.directorate_code = "TestDD"
        self.cost_centre_code = 109076

        group = DepartmentalGroupFactory(
            group_code=self.group_code,
            group_name=self.group_name,
        )
        self.directorate = DirectorateFactory(
            directorate_code=self.directorate_code,
            directorate_name=self.directorate_name,
            group=group,
        )
        self.cost_centre = CostCentreFactory(
            directorate=self.directorate,
            cost_centre_code=self.cost_centre_code,
        )
        current_year = get_current_financial_year()
        amount_apr = -9876543
        self.programme_obj = ProgrammeCodeFactory()

        expenditure_obj = ExpenditureCategoryFactory()
        self.expenditure_id = expenditure_obj.id
        nac_obj = NaturalCodeFactory(natural_account_code=12345678,
                                     expenditure_category=expenditure_obj,
                                     economic_budget_code='RESOURCE'
                                     )

        year_obj = FinancialYear.objects.get(financial_year=current_year)

        apr_period = FinancialPeriod.objects.get(financial_period_code=1)
        apr_period.actual_loaded = True
        apr_period.save()

        # If you use the MonthlyFigureFactory the test fails.
        # I cannot work out why, it may be due to using a random year....
        financial_code_obj = FinancialCode.objects.create(
            programme=self.programme_obj,
            cost_centre=self.cost_centre,
            natural_account_code=nac_obj,
        )
        financial_code_obj.save
        self.forecast_expenditure_type_id = \
            financial_code_obj.forecast_expenditure_type.forecast_expenditure_type_name
        apr_figure = ForecastMonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=1
            ),
            amount=amount_apr,
            financial_code=financial_code_obj,
            financial_year=year_obj
        )
        apr_figure.save

        self.amount_may = 1234567
        may_figure = ForecastMonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=4
            ),
            financial_code=financial_code_obj,
            financial_year=year_obj,
            amount=self.amount_may
        )
        may_figure.save

        # Assign forecast view permission
        can_view_forecasts = Permission.objects.get(
            codename='can_view_forecasts'
        )
        self.test_user.user_permissions.add(can_view_forecasts)
        self.test_user.save()

        # Bust permissions cache (refresh_from_db does not work)
        self.test_user, _ = get_user_model().objects.get_or_create(
            email=TEST_EMAIL
        )

        self.budget = create_budget(financial_code_obj, year_obj)
        self.year_total = amount_apr + self.amount_may
        self.underspend_total = self.budget - amount_apr - self.amount_may
        self.spend_to_date_total = amount_apr

    def check_programme_details_table(self, table):
        details_rows = table.find_all("tr")

        last_details_cols = details_rows[-1].find_all("td")
        # Check the total for the year
        assert last_details_cols[TOTAL_COLUMN].get_text().strip() == \
            format_forecast_figure(self.year_total / 100)
        # Check the difference between budget and year total
        assert last_details_cols[UNDERSPEND_COLUMN].get_text().strip() == \
            format_forecast_figure(self.underspend_total / 100)
        # Check the spend to date
        assert last_details_cols[SPEND_TO_DATE_COLUMN].get_text().strip() == \
            format_forecast_figure(self.spend_to_date_total / 100)

    def check_negative_value_formatted(self, soup, lenght):
        negative_values = soup.find_all("span", class_="negative")
        assert len(negative_values) == lenght

    def check_response(self, resp):
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "govuk-table")

        soup = BeautifulSoup(resp.content, features="html.parser")

        # Check that there is 1 table
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 1

        # Check that all the subtotal hierachy_rows exist
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 3
        self.check_negative_value_formatted(soup, 6)

        # Check that the only table displays  the correct totals
        self.check_programme_details_table(tables[0])

    def test_view_directory_programme_details(self):
        resp = self.client.get(
            reverse(
                "programme_details_directorate",
                kwargs={
                    'directorate_code': self.directorate.directorate_code,
                    'programme_code': self.programme_obj.programme_code,
                    'forecast_expenditure_type': self.forecast_expenditure_type_id,
                    'period': 0,
                },
            )
        )
        self.check_response(resp)

    def test_view_group_programme_details(self):
        resp = self.client.get(
            reverse(
                "programme_details_group",
                kwargs={
                    'group_code': self.group_code,
                    'programme_code': self.programme_obj.programme_code,
                    'forecast_expenditure_type': self.forecast_expenditure_type_id,
                    'period': 0,
                },
            )
        )

        self.check_response(resp)

    def test_view_dit_programme_details(self):
        resp = self.client.get(
            reverse(
                "programme_details_dit",
                kwargs={
                    'programme_code': self.programme_obj.programme_code,
                    'forecast_expenditure_type': self.forecast_expenditure_type_id,
                    'period': 0,
                },
            )
        )
        self.check_response(resp)


class ViewEditButtonTest(BaseTestCase):
    def setUp(self):
        # Add forecast view permission
        can_view_forecasts = Permission.objects.get(
            codename='can_view_forecasts'
        )

        self.test_user.user_permissions.add(can_view_forecasts)
        self.test_user.save()

        self.client.force_login(self.test_user)

        self.group = DepartmentalGroupFactory()

        self.directorate = DirectorateFactory(
            group=self.group,
        )

        self.test_cost_centre = 888812
        self.cost_centre_code = self.test_cost_centre
        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )

    def test_user_can_view_edit_button(self):
        """
        Test user has Edit Forecast permissions to view specific cost centre
        """

        assign_perm("change_costcentre", self.test_user, self.cost_centre)

        # Takes the client to the 'View Forecast' tab for a specified Cost Centre
        view_forecast_url = reverse(
            "forecast_cost_centre",
            kwargs={
                'cost_centre_code': self.cost_centre_code,
                "period": 0,
            }
        )

        response = self.client.get(view_forecast_url)
        assert response.status_code == 200

        soup = BeautifulSoup(response.content, features="html.parser")

        # Looks for 'edit-forecast-link' class (Edit Forecast Button), returns '1'
        # Proves 'Edit Forecast' appears on page as user has editing perm for CC.
        edit_forecast_links = soup.find_all("a", class_="edit-forecast-link")

        assert len(edit_forecast_links) == 1

    def test_user_cannot_view_edit_button(self):
        """
        Tests 'Edit Forecast' button does not appear when
        user has not been assigned editing permissions.
        """
        view_forecast_url = reverse(
            "forecast_cost_centre",
            kwargs={
                'cost_centre_code': self.cost_centre_code,
                "period": 0,
            }
        )

        response = self.client.get(view_forecast_url)
        assert response.status_code == 200

        soup = BeautifulSoup(response.content, features="html.parser")

        # Looks for 'edit-forecast-link' class (Edit Forecast Button) returns '[]'
        edit_forecast_links = soup.find_all("a", class_="edit-forecast-link")

        assert len(edit_forecast_links) == 0

    def test_user_cannot_view_unassigned_cost_centre(self):
        """
        Tests user can view a cost centre but cannot see
        'Edit Forecast' button as they do not have the permissions.
        """

        # Assigns user to one cost centre
        assign_perm("change_costcentre", self.test_user, self.cost_centre)

        # Changes cost_centre_code to one that user can view but NOT edit
        self.test_cost_centre = 888332
        self.cost_centre_code = self.test_cost_centre
        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )

        # Client to 'View Forecast' tab for Cost Centre they cannot edit
        view_forecast_url = reverse(
            "forecast_cost_centre",
            kwargs={
                'cost_centre_code': self.cost_centre_code,
                "period": 0,
            }
        )
        response = self.client.get(view_forecast_url)
        assert response.status_code == 200

        soup = BeautifulSoup(response.content, features="html.parser")

        # Tests that user cannot see 'Edit Forecast' button
        edit_forecast_links = soup.find_all("a", class_="edit-forecast-link")

        assert len(edit_forecast_links) == 0


class ViewForecastHierarchyZeroProjectTest(BaseTestCase):
    # Test that nothing is displayed when there are values
    # that aggregate to 0
    def setUp(self):
        self.group_name = "Test Group"
        self.group_code = "TestGG"
        self.directorate_name = "Test Directorate"
        self.directorate_code = "TestDD"
        self.cost_centre_code = 109076

        self.group = DepartmentalGroupFactory(
            group_code=self.group_code,
            group_name=self.group_name,
        )
        self.directorate = DirectorateFactory(
            directorate_code=self.directorate_code,
            directorate_name=self.directorate_name,
            group=self.group,
        )
        self.cost_centre = CostCentreFactory(
            directorate=self.directorate,
            cost_centre_code=self.cost_centre_code,
        )
        self.cost_centre1 = CostCentreFactory(
            directorate=self.directorate,
            cost_centre_code=109070,
        )
        current_year = get_current_financial_year()
        self.amount_apr = 1234567
        self.programme_obj = ProgrammeCodeFactory()
        nac_obj = NaturalCodeFactory()
        self.project_obj = ProjectCodeFactory()
        year_obj = FinancialYear.objects.get(financial_year=current_year)

        apr_period = FinancialPeriod.objects.get(financial_period_code=1)
        apr_period.actual_loaded = True
        apr_period.save()

        # If you use the MonthlyFigureFactory the test fails.
        # I cannot work out why, it may be due to using a random year....
        financial_code_obj = FinancialCode.objects.create(
            programme=self.programme_obj,
            cost_centre=self.cost_centre,
            natural_account_code=nac_obj,
            project_code=self.project_obj
        )
        financial_code_obj.save
        financial_code_obj1 = FinancialCode.objects.create(
            programme=self.programme_obj,
            cost_centre=self.cost_centre1,
            natural_account_code=nac_obj,
            project_code=self.project_obj
        )
        financial_code_obj1.save
        apr_figure = ForecastMonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=1
            ),
            financial_code=financial_code_obj,
            financial_year=year_obj,
            amount=self.amount_apr
        )
        apr_figure.save

        apr_figure = ForecastMonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=1
            ),
            financial_code=financial_code_obj1,
            financial_year=year_obj,
            amount=-self.amount_apr
        )
        apr_figure.save

        self.amount_may = 891000
        may_figure = ForecastMonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=2,
            ),
            amount=self.amount_may,
            financial_code=financial_code_obj,
            financial_year=year_obj
        )
        may_figure.save

        may_figure = ForecastMonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=2,
            ),
            amount=-self.amount_may,
            financial_code=financial_code_obj1,
            financial_year=year_obj
        )
        may_figure.save

        # Assign forecast view permission
        can_view_forecasts = Permission.objects.get(
            codename='can_view_forecasts'
        )
        self.test_user.user_permissions.add(can_view_forecasts)
        self.test_user.save()

        self.client.force_login(self.test_user)

    def test_view_directorate_summary(self):
        resp = self.client.get(
            reverse(
                "forecast_directorate",
                kwargs={
                    'directorate_code': self.directorate.directorate_code,
                    'period': 0,
                },
            )
        )

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "govuk-table")
        soup = BeautifulSoup(resp.content, features="html.parser")

        # Check that there are 4 tables on the page
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 4

        # Check that all the tables are empty
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 8

    def test_view_group_summary(self):
        response = self.client.get(
            reverse(
                "forecast_group",
                kwargs={
                    'group_code': self.group.group_code,
                    'period': 0,
                },
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "govuk-table")
        soup = BeautifulSoup(response.content, features="html.parser")

        # Check that there are 4 tables on the page
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 4

        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 4

    def test_view_dit_summary(self):
        response = self.client.get(
            reverse(
                "forecast_dit",
                kwargs={
                    'period': 0,
                },
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "govuk-table")
        soup = BeautifulSoup(response.content, features="html.parser")

        # Check that there are 4 tables on the page
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 4

        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 4
