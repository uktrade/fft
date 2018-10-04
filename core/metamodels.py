from django.contrib.admin.models import ADDITION, CHANGE, LogEntry
from django.contrib.contenttypes.models import ContentType
from django.db import models
from core.middleware import get_current_user

class TimeStampedModel(models.Model):
    """ An abstract base class model that provide self-updating
    'created' and 'modified' field, and an active flag"""
    active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class LogChangeModel(models.Model):
    """An abstract base class that saves the changes to a log table.
    https://stackoverflow.com/questions/1355150/django-when-saving-how-can-you-check-if-a-field-has-changed
    """
    excludelist = ['created', 'updated']
    _original_values = {}

    @classmethod
    def from_db(cls, db, field_names, values):
        # https://docs.djangoproject.com/en/2.0/ref/models/instances/
        instance = super(LogChangeModel, cls).from_db(db, field_names,
                                                      values)  #
        # customization to store the original field values on the instance
        d = dict(zip(field_names, values))
        instance._original_values = {f: v for f, v in d.items() if f not in instance.excludelist}
        return instance

    def save(self, *args, **kwargs):
        # check what has changed
        message = ''
        changed = False
        if self._state.adding is True:
            changed = True
            flag = ADDITION
            message = 'Created'
        else:
            flag = CHANGE
            for k, v in self._original_values.items():
                newvalue = getattr(self, k)
                if newvalue != v:
                    message = message + ' ' + self._meta.get_field(k).verbose_name + \
                        ' changed from "' + str(v) + '" to "' + str(newvalue) + '";'
                    self._original_values[k] = newvalue
                    changed = True
        if changed:
            # write to the Admin history log the list of changes
            message = '<' + self.__class__.__name__ + ' ' + self.__str__() + '>  ' + message
            userid = get_current_user()
            #userid = 1
            ct = ContentType.objects.get_for_model(self)
            LogEntry.objects.log_action(
                user_id=userid,
                content_type_id=ct.pk,
                object_id=self.pk,
                object_repr=self.__str__(),
                action_flag=flag,
                change_message=message)
        # maybe it should not be saved if nothing has changed, but I need to think about it
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    class Meta:
        abstract = True
