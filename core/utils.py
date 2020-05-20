import datetime
from enum import Enum

from django.contrib.admin.models import (
    CHANGE,
    LogEntry,
)
from django.contrib.contenttypes.models import ContentType


# to use enum in the models
class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)


def today_string():
    today = datetime.datetime.today()
    return today.strftime("%d %b %Y")


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
