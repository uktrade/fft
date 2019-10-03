import datetime
from enum import Enum


# to use enum in the models
class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)


def today_string():
    today = datetime.datetime.today()
    return today.strftime('%d %b %Y')


FINANCIAL_YEAR_MONTHS = [
    ('Apr', 'April'),
    ('May', 'May'),
    ('Jun', 'June'),
    ('Jul', 'July'),
]

FULL_YEAR = ['apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'jan', 'feb', 'mar']

