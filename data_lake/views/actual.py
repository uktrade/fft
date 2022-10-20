from core.utils.generic_helpers import get_current_financial_year
from data_lake.views.data_lake_view import DataLakeViewSet
from data_lake.views.utils import FigureFieldData
from forecast.models import FinancialPeriod, ForecastMonthlyFigure
from previous_years.models import ArchivedForecastData


class ActualViewSet(DataLakeViewSet, FigureFieldData):
    filename = "actual"
    actual_title = [
        "Actual",
        "Financial Period Code",
        "Financial Period Name",
        "Year",
    ]
    title_list = FigureFieldData.chart_of_account_titles.copy()
    title_list.extend(actual_title)

    def process_row(self, row, writer):
        year = row["financial_year_id"]
        for info in self.period_info:
            month = info[1]
            period_code = info[0]
            if row[month.lower()]:
                output_row = [
                    row[self.cost_centre_field],
                    row[self.nac_field],
                    row[self.programme_field],
                    row[self.contract_field],
                    row[self.market_field],
                    row[self.project_field],
                    row[self.expenditure_type_field],
                    row[self.expenditure_type_description_field],
                    row[month.lower()],
                    period_code,
                    month,
                    year,
                ]
                writer.writerow(output_row)

    def write_data(self, writer):
        current_year = get_current_financial_year()
        self.set_fields()
        # Current year actuals
        actual_period_list = (
            FinancialPeriod.financial_period_info.actual_period_code_list()
        )
        actual_queryset = (
            ForecastMonthlyFigure.objects.exclude(amount=0)
            .select_related(*self.select_related_list)
            .filter(archived_status__isnull=True)
            .filter(financial_year_id=current_year)
            .filter(financial_period_id__in=actual_period_list)
            .values_list(
                *self.chart_of_account_field_list,
                "amount",
                "financial_period__financial_period_code",
                "financial_period__period_short_name",
                "financial_year_id",
            )
        )

        for row in actual_queryset:
            writer.writerow(row)

        self.period_info = FinancialPeriod.objects.all().values_list(
            "financial_period_code", "period_short_name"
        )

        # Previous year actuals
        actual_queryset = (
            ArchivedForecastData.objects.exclude(budget=0).select_related(
                *self.select_related_list
            )
        ).values(
            *self.chart_of_account_field_list,
            "apr",
            "may",
            "jun",
            "jul",
            "aug",
            "sep",
            "oct",
            "nov",
            "dec",
            "jan",
            "feb",
            "mar",
            "adj1",
            "adj2",
            "adj3",
            "financial_year_id",
        )

        for row in actual_queryset:
            self.process_row(row, writer)
