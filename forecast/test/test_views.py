from bs4 import BeautifulSoup

from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.urls import reverse

from chartofaccountDIT.test.factories import (
    Analysis1Factory,
    Analysis2Factory,
    ExpenditureCategoryFactory,
    NaturalCodeFactory,
    ProgrammeCodeFactory,
    ProjectCodeFactory,
)

from core.models import FinancialYear
from core.myutils import get_current_financial_year
from core.test.test_base import RequestFactoryBase

from costcentre.test.factories import (
    CostCentreFactory,
    DepartmentalGroupFactory,
    DirectorateFactory,
)

from forecast.models import (
    FinancialCode,
    FinancialPeriod,
    MonthlyFigure,
    MonthlyFigureAmount,
)
from forecast.permission_shortcuts import assign_perm
from forecast.test.factories import (
    ForecastPermissionFactory,
)
from forecast.views.edit_forecast import (
    AddRowView,
    ChooseCostCentreView,
    EditForecastView,
)
from forecast.views.view_forecast.expenditure_details import (
    CostCentreExpenditureDetailsView,
    DITExpenditureDetailsView,
    DirectorateExpenditureDetailsView,
    GroupExpenditureDetailsView,
)
from forecast.views.view_forecast.forecast_summary import (
    CostCentreView,
    DITView,
    DirectorateView,
    GroupView,
)
from forecast.views.view_forecast.programme_details import (
    DITProgrammeDetailsView,
    DirectorateProgrammeDetailsView,
    GroupProgrammeDetailsView,
)

TOTAL_COLUMN = -3
SPEND_TO_DATE_COLUMN = -4
UNDERSPEND_COLUMN = -2

HIERARCHY_TABLE_INDEX = 0
PROGRAMME_TABLE_INDEX = 1
EXPENDITURE_TABLE_INDEX = 2
PROJECT_TABLE_INDEX = 3


def format_forecast_figure(value):
    return f'{round(value):,d}'


class ViewPermissionsTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)

        self.test_cost_centre = 888812
        self.cost_centre_code = self.test_cost_centre
        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )

    def test_edit_forecast_view_permission(self):
        edit_forecast_url = reverse(
            "edit_forecast",
            kwargs={
                'cost_centre_code': self.cost_centre_code
            }
        )

        # Should 403 as they do not have permission
        with self.assertRaises(PermissionDenied):
            self.factory_get(
                edit_forecast_url,
                EditForecastView,
                cost_centre_code=self.cost_centre_code,
            )

    def test_edit_forecast_view(self):
        # Add forecast view permission
        ForecastPermissionFactory(
            user=self.test_user,
        )

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

        resp = self.factory_get(
            edit_forecast_url,
            EditForecastView,
            cost_centre_code=self.cost_centre_code,
        )

        # Should have been redirected (no permission)
        self.assertEqual(resp.status_code, 302)

        assign_perm("change_costcentre", self.test_user, self.cost_centre)
        assign_perm("view_costcentre", self.test_user, self.cost_centre)

        self.assertTrue(self.test_user.has_perm("change_costcentre", self.cost_centre))
        self.assertTrue(self.test_user.has_perm("view_costcentre", self.cost_centre))

        resp = self.factory_get(
            edit_forecast_url,
            EditForecastView,
            cost_centre_code=self.cost_centre_code,
        )

        # Should be allowed
        self.assertEqual(resp.status_code, 200)


class AddForecastRowTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)

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
        return self.factory_get(
            url,
            AddRowView,
            cost_centre_code=self.cost_centre_code,
        )

    def add_row_post_response(self, url, post_content):
        return self.factory_post(
            url,
            post_content,
            AddRowView,
            cost_centre_code=self.cost_centre_code,
        )

    def edit_row_get_response(self):
        edit_view_url = reverse(
            "edit_forecast",
            kwargs={
                'cost_centre_code': self.cost_centre_code
            },
        )

        return self.factory_get(
            edit_view_url,
            EditForecastView,
            cost_centre_code=self.cost_centre_code,
        )

    def test_view_add_row(self):
        assign_perm("change_costcentre", self.test_user, self.cost_centre)
        assign_perm("view_costcentre", self.test_user, self.cost_centre)

        monthly_figures = MonthlyFigure.objects.all()

        assert monthly_figures.count() == 0

        add_resp = self.add_row_get_response(
            reverse(
                "add_forecast_row",
                kwargs={
                    'cost_centre_code': self.cost_centre_code
                },
            )
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
            }
        )

        self.assertEqual(add_row_resp.status_code, 302)

        assert monthly_figures.count() == 12

    def test_duplicate_values_invalid(self):
        assign_perm("change_costcentre", self.test_user, self.cost_centre)
        assign_perm("view_costcentre", self.test_user, self.cost_centre)

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
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(MonthlyFigure.objects.count(), 12)

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
            }
        )

        self.assertEqual(response_2.status_code, 200)

        assert "govuk-list govuk-error-summary__list" in str(
            response_2.rendered_content,
        )
        self.assertEqual(MonthlyFigure.objects.count(), 12)


class ChooseCostCentreTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)

        self.cost_centre_code = 109076
        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )
        assign_perm("change_costcentre", self.test_user, self.cost_centre)
        assign_perm("view_costcentre", self.test_user, self.cost_centre)

    def test_choose_cost_centre(self):
        response = self.factory_get(
            reverse(
                "choose_cost_centre"
            ),
            ChooseCostCentreView,
            kwargs={
                'cost_centre_code': self.cost_centre_code
            },  # required because factory does not pass kwargs to request
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        response = self.factory_post(
            reverse(
                "choose_cost_centre"
            ), {
                "cost_centre": self.cost_centre_code
            },
            ChooseCostCentreView,
            kwargs={
                'cost_centre_code': self.cost_centre_code
            },  # required because factory does not pass kwargs to request
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        # Check we've been forwarded to edit page
        assert "/forecast/edit/" in response.url


class ViewForecastHierarchyTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)

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
        self.amount_apr = -9876543
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
        apr_figure = MonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=1
            ),
            financial_code=financial_code_obj,
            financial_year=year_obj
        )
        apr_figure.save
        apr_amount = MonthlyFigureAmount.objects.create(
            version=1,
            monthly_figure=apr_figure,
            amount=self.amount_apr
        )
        apr_amount.save()
        self.amount_may = 1234567
        may_figure = MonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=4
            ),
            financial_code=financial_code_obj,
            financial_year=year_obj
        )
        may_figure.save
        may_amount = MonthlyFigureAmount.objects.create(
            version=1,
            monthly_figure=may_figure,
            amount=self.amount_may
        )
        may_amount.save()
        # Assign forecast view permission
        ForecastPermissionFactory(
            user=self.test_user,
        )
        self.year_total = self.amount_apr + self.amount_may
        self.underspend_total = -self.amount_apr - self.amount_may
        self.spend_to_date_total = self.amount_apr

    def test_dit_view(self):
        response = self.factory_get(
            reverse("forecast_dit"),
            DITView,
        )

        self.assertEqual(response.status_code, 200)

        # Check group is shown
        assert self.group_name in str(response.rendered_content)

    def test_group_view(self):
        response = self.factory_get(
            reverse(
                "forecast_group",
                kwargs={
                    'group_code': self.group.group_code
                },
            ),
            GroupView,
            group_code=self.group.group_code,
        )
        self.assertEqual(response.status_code, 200)

        # Check directorate is shown
        assert self.directorate_name in str(response.rendered_content)

    def test_directorate_view(self):
        response = self.factory_get(
            reverse(
                "forecast_directorate",
                kwargs={
                    'directorate_code': self.directorate.directorate_code
                },
            ),
            DirectorateView,
            directorate_code=self.directorate.directorate_code,
        )
        self.assertEqual(response.status_code, 200)

        # Check cost centre is shown
        assert str(self.cost_centre_code) in str(response.rendered_content)

    def test_cost_centre_view(self):
        response = self.factory_get(
            reverse(
                "forecast_cost_centre",
                kwargs={
                    'cost_centre_code': self.cost_centre_code
                },
            ),
            CostCentreView,
            cost_centre_code=self.cost_centre.cost_centre_code,
        )
        self.assertEqual(response.status_code, 200)

        # Check directorate is shown
        assert str(self.cost_centre_code) in str(response.rendered_content)

    def check_programme_table(self, table, prog_index=2):
        programme_rows = table.find_all("tr")
        first_prog_cols = programme_rows[1].find_all("td")
        assert first_prog_cols[prog_index].get_text() == \
            self.programme_obj.programme_description
        assert first_prog_cols[prog_index + 1].get_text() == \
            self.programme_obj.programme_code

        last_programme_cols = programme_rows[-1].find_all("td")
        # Check the total for the year
        assert last_programme_cols[TOTAL_COLUMN].get_text() == \
            format_forecast_figure(self.year_total / 100)
        # Check the difference between budget and year total
        assert last_programme_cols[UNDERSPEND_COLUMN].get_text() == \
            format_forecast_figure(self.underspend_total / 100)
        # Check the spend to date
        assert last_programme_cols[SPEND_TO_DATE_COLUMN].get_text() == \
            format_forecast_figure(self.spend_to_date_total / 100)

    def check_expenditure_table(self, table):
        expenditure_rows = table.find_all("tr")
        first_expenditure_cols = expenditure_rows[1].find_all("td")
        assert (first_expenditure_cols[1].get_text() == '—')

        last_expenditure_cols = expenditure_rows[-1].find_all("td")
        # Check the total for the year
        assert last_expenditure_cols[TOTAL_COLUMN].get_text() == \
            format_forecast_figure(self.year_total / 100)
        # Check the difference between budget and year total
        assert last_expenditure_cols[UNDERSPEND_COLUMN].get_text() == \
            format_forecast_figure(self.underspend_total / 100)
        # Check the spend to date
        assert last_expenditure_cols[SPEND_TO_DATE_COLUMN].get_text() == \
            format_forecast_figure(self.spend_to_date_total / 100)

    def check_project_table(self, table):
        project_rows = table.find_all("tr")
        first_project_cols = project_rows[1].find_all("td")
        assert first_project_cols[1].get_text() == self.project_obj.project_description
        assert first_project_cols[2].get_text() == self.project_obj.project_code

        last_project_cols = project_rows[-1].find_all("td")
        # Check the total for the year
        assert last_project_cols[TOTAL_COLUMN].get_text() == \
            format_forecast_figure(self.year_total / 100)
        # Check the difference between budget and year total
        assert last_project_cols[UNDERSPEND_COLUMN].get_text() == \
            format_forecast_figure(self.underspend_total / 100)
        # Check the spend to date
        assert last_project_cols[SPEND_TO_DATE_COLUMN].get_text() == \
            format_forecast_figure(self.spend_to_date_total / 100)

    def check_hierarchy_table(self, table, hierarchy_element):
        hierarchy_rows = table.find_all("tr")
        first_hierarchy_cols = hierarchy_rows[1].find_all("td")

        assert first_hierarchy_cols[1].get_text() == hierarchy_element
        # Check the April value
        assert first_hierarchy_cols[4].get_text() == format_forecast_figure(
            self.amount_apr / 100
        )
        last_hierarchy_cols = hierarchy_rows[-1].find_all("td")
        # Check the total for the year
        assert last_hierarchy_cols[TOTAL_COLUMN].get_text() == \
            format_forecast_figure(self.year_total / 100)
        # Check the difference between budget and year total
        assert last_hierarchy_cols[UNDERSPEND_COLUMN].get_text() == \
            format_forecast_figure(self.underspend_total / 100)
        # Check the spend to date
        assert last_hierarchy_cols[SPEND_TO_DATE_COLUMN].get_text() == \
            format_forecast_figure(self.spend_to_date_total / 100)

    def check_negative_value_formatted(self, soup):
        negative_values = soup.find_all("span", class_="negative")
        assert len(negative_values) == 42

    def test_view_cost_centre_summary(self):
        resp = self.factory_get(
            reverse(
                "forecast_cost_centre",
                kwargs={
                    'cost_centre_code': self.cost_centre_code
                },
            ),
            CostCentreView,
            cost_centre_code=self.cost_centre_code,
        )

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "govuk-table")
        soup = BeautifulSoup(resp.content, features="html.parser")

        # Check that there are 4 tables on the page
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 4

        # Check that the first table displays the cost centre code

        # Check that all the subtotal hierachy_rows exist
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 18

        self.check_negative_value_formatted(soup)

        self.check_hierarchy_table(tables[HIERARCHY_TABLE_INDEX],
                                   self.cost_centre.cost_centre_name)
        # Check that the second table displays the programme and the correct totals
        # The programme table in the cost centre does not show the 'View'
        # so the programme is displayed in a different column
        self.check_programme_table(tables[PROGRAMME_TABLE_INDEX], 1)

        # Check that the third table displays the expenditure and the correct totals
        self.check_expenditure_table(tables[EXPENDITURE_TABLE_INDEX])

        # Check that the second table displays the project and the correct totals
        self.check_project_table(tables[PROJECT_TABLE_INDEX])

    def test_view_directorate_summary(self):
        resp = self.factory_get(
            reverse(
                "forecast_directorate",
                kwargs={
                    'directorate_code': self.directorate.directorate_code
                },
            ),
            DirectorateView,
            directorate_code=self.directorate.directorate_code,
        )

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "govuk-table")
        soup = BeautifulSoup(resp.content, features="html.parser")

        # Check that there are 4 tables on the page
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 4

        # Check that the first table displays the cost centre code

        # Check that all the subtotal hierachy_rows exist
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 18

        self.check_negative_value_formatted(soup)

        self.check_hierarchy_table(tables[HIERARCHY_TABLE_INDEX],
                                   self.cost_centre.cost_centre_name)
        # Check that the second table displays the programme and the correct totals
        self.check_programme_table(tables[PROGRAMME_TABLE_INDEX])

        # Check that the third table displays the expenditure and the correct totals
        self.check_expenditure_table(tables[EXPENDITURE_TABLE_INDEX])

        # Check that the second table displays the project and the correct totals
        self.check_project_table(tables[PROJECT_TABLE_INDEX])

    def test_view_group_summary(self):
        response = self.factory_get(
            reverse(
                "forecast_group",
                kwargs={
                    'group_code': self.group.group_code
                },
            ),
            GroupView,
            group_code=self.group.group_code,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "govuk-table")
        soup = BeautifulSoup(response.content, features="html.parser")

        # Check that there are 4 tables on the page
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 4

        # Check that the first table displays the cost centre code

        # Check that all the subtotal hierachy_rows exist
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 18

        self.check_negative_value_formatted(soup)

        self.check_hierarchy_table(tables[HIERARCHY_TABLE_INDEX],
                                   self.directorate.directorate_name)
        # Check that the second table displays the programme and the correct totals
        self.check_programme_table(tables[PROGRAMME_TABLE_INDEX])

        # Check that the third table displays the expenditure and the correct totals
        self.check_expenditure_table(tables[EXPENDITURE_TABLE_INDEX])

        # Check that the second table displays the project and the correct totals
        self.check_project_table(tables[PROJECT_TABLE_INDEX])

    def test_view_dit_summary(self):
        response = self.factory_get(
            reverse("forecast_dit"),
            DITView,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "govuk-table")
        soup = BeautifulSoup(response.content, features="html.parser")

        # Check that there are 4 tables on the page
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 4

        # Check that the first table displays the cost centre code

        # Check that all the subtotal hierarchy_rows exist
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 18

        self.check_negative_value_formatted(soup)

        self.check_hierarchy_table(tables[HIERARCHY_TABLE_INDEX],
                                   self.group_name)
        # Check that the second table displays the programme and the correct totals
        self.check_programme_table(tables[PROGRAMME_TABLE_INDEX])

        # Check that the third table displays the expenditure and the correct totals
        self.check_expenditure_table(tables[EXPENDITURE_TABLE_INDEX])

        # Check that the second table displays the project and the correct totals
        self.check_project_table(tables[PROJECT_TABLE_INDEX])


class ViewForecastNaturalAccountCodeTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)

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
        self.budget_type = programme_obj.budget_type_fk.budget_type_display
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
        apr_figure = MonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=1
            ),
            financial_code=financial_code1_obj,
            financial_year=year_obj
        )
        apr_figure.save
        apr_amount = MonthlyFigureAmount.objects.create(
            version=1,
            monthly_figure=apr_figure,
            amount=self.amount1_apr
        )
        apr_amount.save()

        apr_figure = MonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=1
            ),
            financial_code=financial_code2_obj,
            financial_year=year_obj
        )
        apr_figure.save
        apr_amount = MonthlyFigureAmount.objects.create(
            version=1,
            monthly_figure=apr_figure,
            amount=self.amount2_apr
        )
        apr_amount.save()

        self.amount_may = 1234567
        may_figure = MonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=4
            ),
            financial_code=financial_code1_obj,
            financial_year=year_obj
        )
        may_figure.save
        may_amount = MonthlyFigureAmount.objects.create(
            version=1,
            monthly_figure=may_figure,
            amount=self.amount_may
        )
        may_amount.save()
        # Assign forecast view permission
        ForecastPermissionFactory(
            user=self.test_user,
        )
        self.year_total = self.amount1_apr + self.amount2_apr + self.amount_may
        self.underspend_total = -self.amount1_apr - self.amount_may - self.amount2_apr
        self.spend_to_date_total = self.amount1_apr + self.amount2_apr

    def check_nac_table(self, table):
        nac_rows = table.find_all("tr")
        first_nac_cols = nac_rows[1].find_all("td")
        assert (first_nac_cols[0].get_text() ==
                self.nac2_obj.natural_account_code_description)

        last_nac_cols = nac_rows[-1].find_all("td")
        # Check the total for the year
        assert last_nac_cols[TOTAL_COLUMN].get_text() == \
            format_forecast_figure(self.year_total / 100)
        # Check the difference between budget and year total
        assert last_nac_cols[UNDERSPEND_COLUMN].get_text() == \
            format_forecast_figure(self.underspend_total / 100)
        # Check the spend to date
        assert last_nac_cols[SPEND_TO_DATE_COLUMN].get_text() == \
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

        self.check_negative_value_formatted(soup, 7)

        # Check that the only table displays the nac and the correct totals
        self.check_nac_table(tables[0])

    def test_view_cost_centre_nac_details(self):
        resp = self.factory_get(
            reverse(
                "expenditure_details_cost_centre",
                kwargs={
                    'cost_centre_code': self.cost_centre_code,
                    'expenditure_category': self.expenditure_id,
                    'budget_type': self.budget_type,
                },
            ),
            CostCentreExpenditureDetailsView,
            cost_centre_code=self.cost_centre_code,
            expenditure_category=self.expenditure_id,
            budget_type=self.budget_type
        )
        self.check_response(resp)

    def test_view_directory_nac_details(self):
        resp = self.factory_get(
            reverse(
                "expenditure_details_directorate",
                kwargs={
                    'directorate_code': self.directorate.directorate_code,
                    'expenditure_category': self.expenditure_id,
                    'budget_type': self.budget_type,
                },
            ),
            DirectorateExpenditureDetailsView,
            directorate_code=self.directorate.directorate_code,
            expenditure_category=self.nac1_obj.expenditure_category_id,
            budget_type=self.budget_type
        )
        self.check_response(resp)

    def test_view_group_nac_details(self):
        resp = self.factory_get(
            reverse(
                "expenditure_details_group",
                kwargs={
                    'group_code': self.group.group_code,
                    'expenditure_category': self.expenditure_id,
                    'budget_type': self.budget_type,
                },
            ),
            GroupExpenditureDetailsView,
            group_code=self.group.group_code,
            expenditure_category=self.nac1_obj.expenditure_category_id,
            budget_type=self.budget_type
        )

        self.check_response(resp)

    def test_view_dit_nac_details(self):
        resp = self.factory_get(
            reverse(
                "expenditure_details_dit",
                kwargs={
                    'expenditure_category': self.expenditure_id,
                    'budget_type': self.budget_type,
                },
            ),
            DITExpenditureDetailsView,
            expenditure_category=self.nac1_obj.expenditure_category_id,
            budget_type=self.budget_type
        )

        self.check_response(resp)


class ViewProgrammeDetailsTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)

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
            financial_code_obj.forecast_expenditure_type_id
        apr_figure = MonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=1
            ),
            financial_code=financial_code_obj,
            financial_year=year_obj
        )
        apr_figure.save

        apr_amount = MonthlyFigureAmount.objects.create(
            version=1,
            monthly_figure=apr_figure,
            amount=amount_apr
        )
        apr_amount.save()

        self.amount_may = 1234567
        may_figure = MonthlyFigure.objects.create(
            financial_period=FinancialPeriod.objects.get(
                financial_period_code=4
            ),
            financial_code=financial_code_obj,
            financial_year=year_obj
        )
        may_figure.save

        may_amount = MonthlyFigureAmount.objects.create(
            version=1,
            monthly_figure=may_figure,
            amount=self.amount_may
        )
        may_amount.save()
        # Assign forecast view permission
        ForecastPermissionFactory(
            user=self.test_user,
        )
        self.year_total = amount_apr + self.amount_may
        self.underspend_total = -amount_apr - self.amount_may
        self.spend_to_date_total = amount_apr

    def check_programme_details_table(self, table):
        details_rows = table.find_all("tr")

        last_details_cols = details_rows[-1].find_all("td")
        # Check the total for the year
        assert last_details_cols[TOTAL_COLUMN].get_text() == \
            format_forecast_figure(self.year_total / 100)
        # Check the difference between budget and year total
        assert last_details_cols[UNDERSPEND_COLUMN].get_text() == \
            format_forecast_figure(self.underspend_total / 100)
        # Check the spend to date
        assert last_details_cols[SPEND_TO_DATE_COLUMN].get_text() == \
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
        resp = self.factory_get(
            reverse(
                "programme_details_directorate",
                kwargs={
                    'directorate_code': self.directorate.directorate_code,
                    'programme_code': self.programme_obj.programme_code,
                    'forecast_expenditure_type': self.forecast_expenditure_type_id,
                },
            ),
            DirectorateProgrammeDetailsView,
            directorate_code=self.directorate.directorate_code,
            programme_code=self.programme_obj.programme_code,
            forecast_expenditure_type=self.forecast_expenditure_type_id
        )
        self.check_response(resp)

    def test_view_group_programme_details(self):
        resp = self.factory_get(
            reverse(
                "programme_details_group",
                kwargs={
                    'group_code': self.group_code,
                    'programme_code': self.programme_obj.programme_code,
                    'forecast_expenditure_type': self.forecast_expenditure_type_id,
                },
            ),
            GroupProgrammeDetailsView,
            group_code=self.group_code,
            programme_code=self.programme_obj.programme_code,
            forecast_expenditure_type=self.forecast_expenditure_type_id
        )

        self.check_response(resp)

    def test_view_dit_programme_details(self):
        resp = self.factory_get(
            reverse(
                "programme_details_dit",
                kwargs={
                    'programme_code': self.programme_obj.programme_code,
                    'forecast_expenditure_type': self.forecast_expenditure_type_id,
                },
            ),
            DITProgrammeDetailsView,
            programme_code=self.programme_obj.programme_code,
            forecast_expenditure_type=self.forecast_expenditure_type_id
        )
        self.check_response(resp)
