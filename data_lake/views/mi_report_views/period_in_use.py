
import csv

from django.http import HttpResponse

from rest_framework.viewsets import ViewSet

from data_lake.views.mi_report_views.utils import (
    ARCHIVED_PERIOD_0_NAME,
 )

from end_of_month.models import EndOfMonthStatus

from forecast.models import FinancialPeriod


class MIReportPeriodInUseDataSet(ViewSet):
    filename = "financial_period_in_use"
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
