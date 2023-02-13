import csv

from django.http import HttpResponse
from rest_framework.viewsets import ViewSet

from forecast.models import FinancialPeriod


class MIFinancialPeriodDataSet(ViewSet):
    filename = "financial_period"
    title_list = [
        "Financial Period Code",
        "Financial Period Name",
    ]

    def list(self, request):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={self.filename}.csv"
        writer = csv.writer(response, csv.excel)
        writer.writerow(self.title_list)
        self.write_data(writer)
        return response

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
