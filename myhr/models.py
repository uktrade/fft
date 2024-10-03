from django.db import models

class Group(models.Model):
    group = models.CharField(max_length=100)
    fte = models.CharField(max_length=100)
    count = models.CharField(max_length=100)

    class Meta:
        abstract = False

