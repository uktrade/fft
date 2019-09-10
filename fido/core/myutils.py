# Collection of useful functions and classes
import datetime

from .models import FinancialYear


def financialyear():
    y = FinancialYear.objects.get(current=True)
    if y:
        currentyear = y.financial_year
    else:
        # If there is a data problem and the current year is not defined,
        # return the financial year for the current date
        # The UK financial year starts in April, so Jan, Feb and Mar are part of the previous year

        currentmonth = datetime.datetime.now().month
        currentyear = datetime.datetime.now().year
        if currentmonth < 4:  # the new financial year  starts in April
            currentyear = currentyear - 1  # before April, the financial year it is one year behind
    return currentyear
