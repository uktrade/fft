from core.models import (
    FinancialYear,
)

from data_lake.views.data_lake_view import DataLakeViewSet

class FinancialYearViewSet(DataLakeViewSet):
    filename = "financial_year"
    title_list = [
        "Financial Year",
        "Financial Year Display",
        "Current",
        "Archived",
    ]

    def write_data(self, writer):
        year_queryset = FinancialYear.objects.all().order_by("financial_year",)

        for obj in year_queryset:
            row = [
                obj.financial_year,
                obj.financial_year_display,
                obj.current,
                obj.archived,
            ]
            writer.writerow(row)