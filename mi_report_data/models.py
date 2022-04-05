from django.db import models

from forecast.models import FinancialCode, FinancialPeriod
# Create your models here.


# financial_code_id, budget, forecast, actual,
# financial_period_id, financial_year_id, archived_period_id


class ReportDataView(models.Model):
    id = models.IntegerField(primary_key=True,)
    financial_code = models.ForeignKey(FinancialCode,
                                       on_delete=models.DO_NOTHING,
                                       related_name="mi_report_data_financial_code"
                                       )
    financial_year_id = models.IntegerField()
    financial_period = models.ForeignKey(
        FinancialPeriod,
        on_delete=models.DO_NOTHING,
        related_name="mi_report_data_financial_period",
    )
    archived_period = models.ForeignKey(
        FinancialPeriod,
        on_delete=models.DO_NOTHING,
        related_name="mi_report_data_archived_period",
    )
    budget = models.BigIntegerField(default=0)
    forecast = models.BigIntegerField(default=0)
    actual = models.BigIntegerField(default=0)

    class Meta:
        managed = False
        db_table = "mi_report_data_query"
