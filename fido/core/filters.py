from django.db import models

import django_filters


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
        }
