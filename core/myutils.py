# Collection of useful functions and classes
import datetime

from .models import FinancialYear


def get_current_financial_year():
    y = FinancialYear.objects.filter(current=True)
    if y:
        current_financial_year = y.last().financial_year
    else:
        # If there is a data problem and the current year is not defined,
        # return the financial year for the current date
        # The UK financial year starts in April, so Jan, Feb and Mar are part of the previous year
        today = datetime.datetime.now()
        currentmonth = today.month
        current_financial_year = today.year
        if currentmonth < 3 or (currentmonth == 4 and today.day <5):
            current_financial_year -= 1  # before 5th April, the financial year it is one year behind the calendar year


    return current_financial_year
