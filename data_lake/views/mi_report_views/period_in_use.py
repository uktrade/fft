from data_lake.views.data_lake_view import DataLakeViewSet
from data_lake.views.mi_report_views.utils import ARCHIVED_PERIOD_0_NAME
from end_of_month.models import EndOfMonthStatus
from forecast.models import FinancialPeriod


class MIReportPeriodInUseDataSet(DataLakeViewSet):
    filename = "financial_period_in_use"
    title_list = [
        "Financial Period Code",
        "Financial Period Name",
    ]

    def write_data(self, writer):
        max_period_id = (
            EndOfMonthStatus.archived_period_objects.get_latest_archived_period()
        )
        # The financial periods that have already been archived,
        # and the current period.
        period_queryset = FinancialPeriod.objects.filter(
            financial_period_code__lte=max_period_id + 1
        ).order_by("financial_period_code")
        # Period 0 is always used.
        # It contains the original budgets, at the beginning of the year
        # Used for calculations in the MI reports
        writer.writerow([0, ARCHIVED_PERIOD_0_NAME])
        for obj in period_queryset:
            row = [
                obj.financial_period_code,
                obj.period_short_name,
            ]
            writer.writerow(row)
