import django_filters
from django.db import models


class MyFilterSet(django_filters.FilterSet):
    """Used icontains as default for string when searching in a form"""

    class Meta:
        filter_overrides = {
            models.CharField: {
                "filter_class": django_filters.CharFilter,
                "extra": lambda f: {"lookup_expr": "icontains"},
            }
        }


class ArchivedFilterSet(MyFilterSet):
    year = 0

    @property
    def qs(self):
        return super(ArchivedFilterSet, self).qs.filter(financial_year=self.year)
