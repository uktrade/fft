from django.db import models
from .utils import ChoiceEnum
from django.utils import timezone
from .metamodels import TimeStampedModel


class AdminInfo(models.Model):
    current_month = models.IntegerField() # 1 for jan, etc, calendar month, not financial
    current_financial_year = models.IntegerField() # 2018 for 2018-19 financial year


class EventLog(TimeStampedModel):
    EventType = models.CharField(max_length=500)


