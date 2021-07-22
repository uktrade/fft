from django.db.models import Value

from core.utils.generic_helpers import get_current_financial_year

from data_lake.views.data_lake_view import DataLakeViewSet
from data_lake.views.utils import FigureFieldData


from end_of_month.models import MonthlyTotalBudget

from forecast.models import ForecastingDataView

from previous_years.models import ArchivedForecastData


class BudgetViewSet(DataLakeViewSet, FigureFieldData):
    filename = "Budget"
    budget_title = [
        "Budget",
        "Year",
        "Archived Financial Period Code",
        "Archived Financial Period Name",
    ]
    title_list = FigureFieldData.chart_of_account_titles.copy()
    title_list.extend(budget_title)

    def write_data(self, writer):
        current_year = get_current_financial_year()
        self.set_fields()
        # Current budgets
        budget_queryset = (
            (
                ForecastingDataView.objects.exclude(budget=0).select_related(
                    *self.select_related_list
                )
            )
            .annotate(year=Value(current_year))
            .values_list(
                *self.chart_of_account_field_list,
                "budget",
                "year",
            )
        )

        for row in budget_queryset:
            writer.writerow(row)

        # Archived current year budgets
        budget_queryset = (
            (
                MonthlyTotalBudget.objects.exclude(amount=0)
                .select_related(*self.select_related_list)
                .select_related("archived_status__archived_period")
            )
            .filter(financial_year_id=current_year)
            .values_list(
                *self.chart_of_account_field_list,
                "amount",
                "financial_year_id",
                "archived_status__archived_period__financial_period_code",
                "archived_status__archived_period__period_short_name",
            )
        )

        for row in budget_queryset:
            writer.writerow(row)

        # Previous year budgets
        budget_queryset = (
            ArchivedForecastData.objects.exclude(budget=0).select_related(
                *self.select_related_list
            )
        ).values_list(
            *self.chart_of_account_field_list,
            "budget",
            "financial_year_id",
        )

        for row in budget_queryset:
            writer.writerow(row)
