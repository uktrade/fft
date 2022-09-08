from core.utils.generic_helpers import get_current_financial_year
from data_lake.views.data_lake_view import DataLakeViewSet
from data_lake.views.utils import FigureFieldData
from upload_split_file.models import SplitPayActualFigure


class ActualSplitViewSet(DataLakeViewSet, FigureFieldData):
    filename = "actual_split"
    actual_title = [
        "Actual",
        "Financial Period Code",
        "Financial Period Name",
        "Year",
    ]
    title_list = FigureFieldData.chart_of_account_titles.copy()
    title_list.extend(actual_title)

    def write_data(self, writer):
        current_year = get_current_financial_year()
        self.set_fields()
        forecast_queryset = (
            SplitPayActualFigure.objects.select_related(*self.select_related_list)
            .filter(financial_year_id=current_year)
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
