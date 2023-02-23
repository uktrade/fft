from data_lake.views.data_lake_view import DataLakeViewSet
from forecast.models import FinancialPeriod


class MIFinancialPeriodDataSet(DataLakeViewSet):
    filename = "financial_period"
    title_list = [
        "Financial Period Code",
        "Financial Period Name",
    ]

    def write_data(self, writer):
        # Financial periods and their names
        # and the current period.
        period_queryset = FinancialPeriod.objects.filter(
            financial_period_code__lte=12
        ).order_by("financial_period_code")

        for obj in period_queryset:
            row = [
                obj.financial_period_code,
                obj.period_short_name,
            ]
            writer.writerow(row)
