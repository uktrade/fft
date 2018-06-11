from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """ An abstract base class model that provide self-updating 'created' and 'modified' field"""
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

