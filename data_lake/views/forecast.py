from core.utils.generic_helpers import get_current_financial_year
from data_lake.views.data_lake_view import DataLakeViewSet
from data_lake.views.utils import FigureFieldData
from forecast.models import FinancialPeriod, ForecastMonthlyFigure


class ForecastViewSet(DataLakeViewSet, FigureFieldData):
    filename = "forecast"
    forecast_title = [
        "Forecast",
        "Financial Period Code",
        "Financial Period Name",
        "Year",
        "Archived Financial Period Code",
        "Archived Financial Period Name",
    ]
    title_list = FigureFieldData.chart_of_account_titles.copy()
    title_list.extend(forecast_title)

    def write_data(self, writer):
        current_year = get_current_financial_year()
        self.set_fields()
        # Current forecast
        forecast_period_list = (
            FinancialPeriod.financial_period_info.forecast_period_code_list()
        )
        forecast_queryset = (
            ForecastMonthlyFigure.objects.exclude(amount=0)
            .select_related(*self.select_related_list)
            .filter(archived_status__isnull=True)
            .filter(financial_year_id=current_year)
            .filter(financial_period_id__in=forecast_period_list)
            .values_list(
                *self.chart_of_account_field_list,
                "amount",
                "financial_period__financial_period_code",
                "financial_period__period_short_name",
                "financial_year_id",
            )
        )

        for row in forecast_queryset:
            writer.writerow(row)

        # Archived  forecast for the previous part of the year
        forecast_queryset = (
            (
                ForecastMonthlyFigure.objects.exclude(amount=0).select_related(
                    *self.select_related_list
                )
            )
            .filter(archived_status__isnull=False)
            .filter(financial_year_id=current_year)
            .values_list(
                *self.chart_of_account_field_list,
                "amount",
                "financial_period__financial_period_code",
                "financial_period__period_short_name",
                "financial_year_id",
                "archived_status__archived_period__financial_period_code",
                "archived_status__archived_period__period_short_name",
            )
        )

        for row in forecast_queryset:
            writer.writerow(row)
