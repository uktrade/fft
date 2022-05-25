from django.core.management.base import BaseCommand

from django.db import connection

from forecast.models import FinancialCode


class Command(BaseCommand):
    help = "Delete all unused financial codes"

    def handle(self, *args, **options):

        # Use sql to delete the figure for performance reason.
        # The sql is 1000 times faster than queryset.delete()
        count_before = FinancialCode.objects.all().count()
        with connection.cursor() as cursor:
            # Remove financial codes not used
            sql_delete = (
                "DELETE FROM forecast_financialcode "
                "WHERE ID NOT IN "
                "(SELECT financial_code_id "
                "FROM  forecast_forecastmonthlyfigure "
                "UNION "
                "SELECT financial_code_id "
                "FROM  end_of_month_monthlytotalbudget "
                "UNION "
                "SELECT financial_code_id "
                "FROM  end_of_month_monthlyoutturn "
                "UNION "
                "SELECT financial_code_id "
                "FROM forecast_budgetmonthlyfigure);"
            )
            cursor.execute(sql_delete)
        deleted_count = count_before - FinancialCode.objects.all().count()
        self.stdout.write(
            self.style.SUCCESS(f"Deleted {deleted_count} unused financial codes.")
        )
