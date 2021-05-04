import datetime

from django.contrib.admin.models import (
    CHANGE,
    LogEntry,
)
from django.contrib.contenttypes.models import ContentType

from core.models import FinancialYear


def get_current_financial_year():
    y = FinancialYear.objects.filter(current=True)
    if y:
        current_financial_year = y.last().financial_year
    else:
        # If there is a data problem
        # and the current year is not
        # defined, return the financial
        # year for the current date
        # The UK financial year starts
        # in April, so Jan, Feb and Mar
        # are part of the previous year
        today = datetime.datetime.now()
        current_month = today.month
        current_financial_year = today.year
        if current_month < 3 or (current_month == 4 and today.day < 5):
            # before 5th April, the financial
            # year it is one year behind the
            # calendar year
            current_financial_year -= (
                1
            )

    return current_financial_year


def get_year_display(year):
    y = FinancialYear.objects.get(financial_year=year)
    if y:
        return y.financial_year_display
    else:
        return "Invalid year"


def create_financial_year_display(year):
    if year < 2000:
        return "Invalid year"
    return f"{year}/{year - 1999}"


def make_financial_year_current(financial_year):
    FinancialYear.objects.all().update(current=False)
    FinancialYear.objects.filter(financial_year=financial_year).update(current=True)


class GetValidYear:
    regex = r'20\d{2}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%04d' % value


def today_string():
    today = datetime.datetime.today()
    return today.strftime("%d %b %Y")


# Classes used to display totals and subtotals when showing Forecast/Actuals
SUB_TOTAL_CLASS = "sub-total"
TOTAL_CLASS = "mid-total"
GRAND_TOTAL_CLASS = "grand-total"


def check_empty(value):
    if value is not None and value != '':
        return value

    return None


def log_object_change(
        requesting_user_id,
        message,
        obj=None,
):
    if obj:
        content_type_id = ContentType.objects.get_for_model(
            obj
        ).pk

        LogEntry.objects.log_action(
            user_id=requesting_user_id,
            content_type_id=content_type_id,
            object_id=obj.pk,
            object_repr=str(obj),
            action_flag=CHANGE,
            change_message=f"{str(obj)} {message}",
        )
    else:
        LogEntry.objects.log_action(
            user_id=requesting_user_id,
            content_type_id=None,
            object_id=None,
            object_repr="",
            action_flag=CHANGE,
            change_message=message,
        )
