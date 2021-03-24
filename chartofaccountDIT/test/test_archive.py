from io import StringIO

from bs4 import BeautifulSoup

from django.core.management import call_command
from django.urls import reverse

from chartofaccountDIT.test.factories import (
    Analysis1Factory,
    Analysis2Factory,
    CommercialCategoryFactory,
    ExpenditureCategoryFactory,
    ProgrammeCodeFactory,
)

from core.test.test_base import BaseTestCase
from core.utils.generic_helpers import get_current_financial_year


class ArchiveAnalysis1Test(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)
        self.out = StringIO()

        self.analysis1_code = 123456
        self.analysis1_description = "Analysis1 description"
        Analysis1Factory(
            analysis1_code=self.analysis1_code,
            analysis1_description=self.analysis1_description,
        )
        current_year = get_current_financial_year()
        self.archive_year = current_year - 1

    def show_historical_view(self):
        response = self.client.get(
            reverse("historical_analysis_1", kwargs={"year": self.archive_year},),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "govuk-table")

        soup = BeautifulSoup(response.content, features="html.parser")
        # Check that there is 1 table
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 1
        return soup

    def test_view_historical_analisys1(self):
        soup = self.show_historical_view()
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 2

        call_command(
            "archive", "Analysis1", year=self.archive_year, stdout=self.out,
        )

        soup = self.show_historical_view()
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 1
        table_rows = soup.find_all("tr", class_="even")
        assert len(table_rows) == 1

        first_cols = table_rows[0].find_all("td")
        assert first_cols[0].get_text().strip() == str(self.analysis1_code)
        assert first_cols[1].get_text().strip() == self.analysis1_description

    def test_archive_multiple_years(self):
        call_command(
            "archive", "Analysis1", year=self.archive_year, stdout=self.out,
        )

        call_command(
            "archive", "Analysis1", year=self.archive_year + 1, stdout=self.out,
        )

        soup = self.show_historical_view()
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 1
        table_rows = soup.find_all("tr", class_="even")
        assert len(table_rows) == 1

        first_cols = table_rows[0].find_all("td")
        assert first_cols[0].get_text().strip() == str(self.analysis1_code)
        assert first_cols[1].get_text().strip() == self.analysis1_description


class ArchiveAnalysis2Test(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)
        self.out = StringIO()

        self.analysis2_code = 123456
        self.analysis2_description = "analysis2 description"
        Analysis2Factory(
            analysis2_code=self.analysis2_code,
            analysis2_description=self.analysis2_description,
        )
        current_year = get_current_financial_year()
        self.archive_year = current_year - 1

    def show_historical_view(self):
        response = self.client.get(
            reverse("historical_analysis_2", kwargs={"year": self.archive_year},)
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "govuk-table")

        soup = BeautifulSoup(response.content, features="html.parser")
        # Check that there is 1 table
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 1
        return soup

    def test_view_historical_analisys2(self):
        soup = self.show_historical_view()
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 2

        call_command(
            "archive", "Analysis2", year=self.archive_year, stdout=self.out,
        )

        soup = self.show_historical_view()
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 1
        table_rows = soup.find_all("tr", class_="even")
        assert len(table_rows) == 1

        first_cols = table_rows[0].find_all("td")
        assert first_cols[0].get_text().strip() == str(self.analysis2_code)
        assert first_cols[1].get_text().strip() == self.analysis2_description

    def test_archive_multiple_years(self):
        call_command(
            "archive", "Analysis2", year=self.archive_year, stdout=self.out,
        )

        call_command(
            "archive", "Analysis2", year=self.archive_year + 1, stdout=self.out,
        )

        soup = self.show_historical_view()
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 1
        table_rows = soup.find_all("tr", class_="even")
        assert len(table_rows) == 1

        first_cols = table_rows[0].find_all("td")
        assert first_cols[0].get_text().strip() == str(self.analysis2_code)
        assert first_cols[1].get_text().strip() == self.analysis2_description


class ArchiveExpenditureCategoryTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)
        self.out = StringIO()

        self.grouping_description = "grouping description"
        self.category_description = "Longer description"
        ExpenditureCategoryFactory(
            grouping_description=self.grouping_description,
            description=self.category_description,
        )
        current_year = get_current_financial_year()
        self.archive_year = current_year - 1

    def show_historical_view(self):
        response = self.client.get(
            reverse(
                "historical_finance_category",
                kwargs={"year": self.archive_year},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "govuk-table")

        soup = BeautifulSoup(response.content, features="html.parser")
        # Check that there is 1 table
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 1
        return soup

    def test_view_historical_view(self):
        soup = self.show_historical_view()
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 2

        call_command(
            "archive", "Expenditure_Cat", year=self.archive_year, stdout=self.out,
        )

        soup = self.show_historical_view()
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 1
        table_rows = soup.find_all("tr", class_="even")
        assert len(table_rows) == 1

        first_cols = table_rows[0].find_all("td")
        assert first_cols[1].get_text().strip() == str(self.grouping_description)
        assert first_cols[2].get_text().strip() == self.category_description

    def test_archive_multiple_years(self):
        call_command(
            "archive", "Expenditure_Cat", year=self.archive_year, stdout=self.out,
        )

        call_command(
            "archive",
            "Expenditure_Cat",
            year=self.archive_year + 1,
            stdout=self.out,
        )

        soup = self.show_historical_view()
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 1
        table_rows = soup.find_all("tr", class_="even")
        assert len(table_rows) == 1

        first_cols = table_rows[0].find_all("td")
        assert first_cols[1].get_text().strip() == str(self.grouping_description)
        assert first_cols[2].get_text().strip() == self.category_description


class ArchiveCommercialCategoryTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)

        self.out = StringIO()

        self.commercial_category = "commercial category"
        self.description = "Longer description"
        CommercialCategoryFactory(
            commercial_category=self.commercial_category, description=self.description,
        )
        current_year = get_current_financial_year()
        self.archive_year = current_year - 1

    def show_historical_view(self):
        response = self.client.get(
            reverse(
                "historical_commercial_category",
                kwargs={"year": self.archive_year},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "govuk-table")

        soup = BeautifulSoup(response.content, features="html.parser")
        # Check that there is 1 table
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 1
        return soup

    def test_view_historical_view(self):
        soup = self.show_historical_view()
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 2

        call_command(
            "archive", "Commercial_Cat", year=self.archive_year, stdout=self.out,
        )

        soup = self.show_historical_view()
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 1
        table_rows = soup.find_all("tr", class_="even")
        assert len(table_rows) == 1

        first_cols = table_rows[0].find_all("td")
        assert first_cols[0].get_text().strip() == str(self.commercial_category)
        assert first_cols[1].get_text().strip() == self.description

    def test_archive_multiple_years(self):
        call_command(
            "archive", "Commercial_Cat", year=self.archive_year, stdout=self.out,
        )

        call_command(
            "archive", "Commercial_Cat", year=self.archive_year + 1, stdout=self.out,
        )

        soup = self.show_historical_view()
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 1
        table_rows = soup.find_all("tr", class_="even")
        assert len(table_rows) == 1

        first_cols = table_rows[0].find_all("td")
        assert first_cols[0].get_text().strip() == str(self.commercial_category)
        assert first_cols[1].get_text().strip() == self.description


class ArchiveProgrammeTest(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.test_user)
        self.out = StringIO()

        obj = ProgrammeCodeFactory()
        self.programme_code = obj.programme_code
        self.programme_description = obj.programme_description
        self.budget_type = obj.budget_type.budget_type
        current_year = get_current_financial_year()
        self.archive_year = current_year - 1
        current_year = get_current_financial_year()
        self.archive_year = current_year - 1

    def show_historical_view(self):
        response = self.client.get(
            reverse(
                "historical_programme_filter",
                kwargs={"year": self.archive_year},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "govuk-table")

        soup = BeautifulSoup(response.content, features="html.parser")
        # Check that there is 1 table
        tables = soup.find_all("table", class_="govuk-table")
        assert len(tables) == 1
        return soup

    def test_view_historical_programme(self):
        soup = self.show_historical_view()
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 2

        call_command(
            "archive", "Programmes", year=self.archive_year, stdout=self.out,
        )

        soup = self.show_historical_view()
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 1
        table_rows = soup.find_all("tr", class_="even")
        assert len(table_rows) == 1

        first_cols = table_rows[0].find_all("td")
        assert first_cols[0].get_text().strip() == str(self.programme_code)
        assert first_cols[1].get_text().strip() == self.programme_description
        assert first_cols[2].get_text().strip() == self.budget_type

    def test_archive_multiple_years(self):
        call_command(
            "archive", "Programmes", year=self.archive_year, stdout=self.out,
        )

        call_command(
            "archive", "Programmes", year=self.archive_year + 1, stdout=self.out,
        )

        soup = self.show_historical_view()
        table_rows = soup.find_all("tr", class_="govuk-table__row")
        assert len(table_rows) == 1
        table_rows = soup.find_all("tr", class_="even")
        assert len(table_rows) == 1

        first_cols = table_rows[0].find_all("td")
        assert first_cols[0].get_text().strip() == str(self.programme_code)
        assert first_cols[1].get_text().strip() == self.programme_description
        assert first_cols[2].get_text().strip() == self.budget_type
