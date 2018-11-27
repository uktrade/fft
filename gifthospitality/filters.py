from core.filters import MyFilterSet

from django.db.models import Q

import django_filters

from .models import GiftAndHospitality


class GiftHospitalityFilter(MyFilterSet):
    """Use a single text box to enter an object name.
    It will search into all available fields
    """
    search_all = django_filters.CharFilter(field_name='', label='',
                                                method='search_all_filter')


    def search_all_filter(self, queryset, name, value):
        return queryset.filter(Q(classification__icontains=value) |
                               Q(group_name__icontains=value) |
                               Q(cost_centre_name__icontains=value) |
                               Q(venue__icontains=value) |
                               Q(reason__icontains=value) |
                               Q(band__icontains=value) |
                               Q(rep__icontains=value) |
                               Q(offer__name__icontains=value) |
                               Q(company_rep__icontains=value) |
                               Q(company_icontains=value) |
                               Q(action_taken__icontains=value) |
                               Q(entered_by__icontains=value) |
                               Q(category__icontains=value) |
                               Q(grade__icontains=value)
                               )

    class Meta(MyFilterSet.Meta):
        model = GiftAndHospitality
        fields = [
            'search_all',
        ]

    @property
    def qs(self):
        myqs = super(GiftHospitalityFilter, self).qs
        return myqs.order_by('classification',
                                               'group_name')
