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




