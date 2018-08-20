import django_filters

from django.db import models
# from django import forms



class MyFilterSet(django_filters.FilterSet):
    """Used icontains as default for string when searching in a form"""
    class Meta:
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                'lookup_expr': 'icontains',
                },
            },
            # models.BooleanField: {
            #     'filter_class': django_filters.BooleanFilter,
            #     'extra': lambda f: {
            #     'widget': forms.CheckboxInput,
            #     },
            # },
    }