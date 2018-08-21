import django_filters

from django.db.models import Q
from core.filters import MyFilterSet
from .models import Programme, CostCentre


class OldCostCentreFilter(MyFilterSet):
    class Meta(MyFilterSet.Meta):
        model = CostCentre
        fields = [
                  'directorate__group',
                  'directorate',
                  'cost_centre_code',
                  'cost_centre_name']

    @property
    def qs(self):
        cc = super(CostCentreFilter, self).qs
        return cc.filter(active=True)

class CostCentreFilter(MyFilterSet):
    # Use a single text box to enter an object name. It will search into group, directorate and cost centre name
    obj_name = django_filters.CharFilter(field_name='', label='Name', method = 'obj_name_filter')
    resposible_name = django_filters.CharFilter(field_name='', label='Responsibility', method = 'responsible_name_filter')

    def obj_name_filter(selfself, queryset, name, value):
        return queryset.filter (Q(directorate__group__group_name__icontains=value) | \
               Q(directorate__directorate_name__icontains=value) | \
               Q(cost_centre_name__icontains=value))

    def responsible_name_filter(selfself, queryset, name, value):
        return queryset.filter (
                                   Q(directorate__group__director_general__name__icontains=value) | Q(directorate__group__director_general__surname__icontains=value) | \
                                   Q(directorate__director__name__icontains=value) | Q(directorate__director__surname__icontains=value) | \
                                   Q(business_partner__name__icontains=value) | Q(business_partner__surname__icontains=value) | \
                                   Q(deputy_director__name__icontains=value) | Q(deputy_director__surname__icontains=value)
                                )



    class Meta(MyFilterSet.Meta):
        model = CostCentre
        fields = [
                    'obj_name',
                    'cost_centre_code'
                  ]

    @property
    def qs(self):
        cc = super(CostCentreFilter, self).qs
        return cc.filter(active=True)


class ProgrammeFilter(MyFilterSet):

    class Meta(MyFilterSet.Meta):
        model = Programme
        fields = [
                  'programme_code',
                  'programme_description',
                  'budget_type'
                  ]

    @property
    def qs(self):
        prog = super(ProgrammeFilter, self).qs
        return prog.filter(DIT_in_use=True)

