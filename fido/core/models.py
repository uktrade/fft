from django.db import models

from .metamodels import TimeStampedModel


class EventLog(TimeStampedModel):
    EventType = models.CharField(max_length=500)


class FinancialYear(models.Model):
    """Key and representation of the financial year"""
    financial_year = models.IntegerField(primary_key=True)
    financial_year_display = models.CharField(max_length=20)
    in_use = models.BooleanField(default=False)

    def __str__(self):
        return str(self.financial_year_display)


class AdminInfo(models.Model):
    """Used for general information for the application.
       The current month is the calendar month, 1 for jan, etc, calendar month, not financial
       Financial year is the first year of the financial year, ie 2018 for 2018-19 financial year
    """
    current_month = models.IntegerField()  #
    current_financial_year = models.ForeignKey(FinancialYear, on_delete=models.PROTECT)
