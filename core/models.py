from django.db import models

from .metamodels import TimeStampedModel


class AdminInfo(models.Model):
    """Used for general information for the application.
       The current month is the calendar month, 1 for jan, etc, calendar month, not financial
       Financial year is the first year of the financial year, ie 2018 for 2018-19 financial year
    """
    current_month = models.IntegerField()  #
    current_financial_year = models.IntegerField()


class EventLog(TimeStampedModel):
    EventType = models.CharField(max_length=500)
