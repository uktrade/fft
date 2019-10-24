from core.middleware import get_current_user

from django.contrib.admin.models import ADDITION, CHANGE, LogEntry
from django.contrib.contenttypes.models import ContentType
from django.db import models


class SimpleTimeStampedModel(models.Model):
    """ An abstract base class model that provide self-updating
    'created' and 'modified' field """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TimeStampedModel(SimpleTimeStampedModel):
    """ An abstract base class model that provide self-updating
    'created' and 'modified' field, and an active flag"""

    active = models.BooleanField(default=False)

    class Meta:
        abstract = True


class LogChangeModel(models.Model):
    """An abstract base class that saves the changes to a log table.
    https://stackoverflow.com/questions/1355150/django-when-saving-how-can-you-check-if-a-field-has-changed
    """

    excludelist = ["created", "updated"]
    _original_values = {}

    @classmethod
    def from_db(cls, db, field_names, values):
        # https://docs.djangoproject.com/en/2.0/ref/models/instances/
        instance = super(LogChangeModel, cls).from_db(db, field_names, values)  #
        # customization to store the original field values on the instance
        d = dict(zip(field_names, values))
        instance._original_values = {
            f: v for f, v in d.items() if f not in instance.excludelist
        }
        return instance

    def save(self, *args, **kwargs):
        import core

        # check what has changed
        message = ""
        changed = False
        if self._state.adding is True:
            changed = True
            flag = ADDITION
            message = "Created"
        else:
            flag = CHANGE
            for k, v in self._original_values.items():
                newvalue = getattr(self, k)
                if newvalue != v:
                    message = (
                        message
                        + " "
                        + self._meta.get_field(k).verbose_name
                        + ' changed from "'
                        + str(v)
                        + '" to "'
                        + str(newvalue)
                        + '";'
                    )
                    self._original_values[k] = newvalue
                    changed = True
        if changed:
            # If you have been called from a test, the userid does not exists, and the save of changes will fail.
            if hasattr(core, "_called_from_test") == False:
                # write to the Admin history log the list of changes
                message = (
                    "<"
                    + self.__class__.__name__
                    + " "
                    + self.__str__()
                    + ">  "
                    + message
                )
                user_id = get_current_user()

                # TODO - verify this with Luiscella
                if user_id:
                    ct = ContentType.objects.get_for_model(self)
                    LogEntry.objects.log_action(
                        user_id=user_id,
                        content_type_id=ct.pk,
                        object_id=self.pk,
                        object_repr=self.__str__(),
                        action_flag=flag,
                        change_message=message,
                    )
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    class Meta:
        abstract = True


class ArchivedModel(models.Model):
    financial_year = models.ForeignKey("core.FinancialYear", on_delete=models.PROTECT)
    archived = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
