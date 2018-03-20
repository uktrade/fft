# Collection of useful functions

import datetime

# Return the financial year for the current date
# The UK financial year starts in April, so Jan, Feb and Mar are part of the previous year
def financialyear():
    currentmonth = datetime.now().month
    currentyear = datetime.now().year
    if currentmonth < 4 : # the new financial year  starts in April
        currentyear = currentyear - 1 # before April, the financial year it is one year behind
    return currentyear

