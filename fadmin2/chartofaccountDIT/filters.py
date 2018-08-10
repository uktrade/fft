import django_filters
from .models import NACCategory, NaturalCode, Analysis1, Analysis2, NACDashboardGrouping
from core.filters import MyFilterSet


class NACFilter(MyFilterSet):
    # directorate__group__group_code = django_filters.CharFilter(label='Group Code',lookup_expr='icontains')
    # directorate__group__group_name = django_filters.CharFilter(label='Group Name',lookup_expr='icontains')
    # directorate__directorate_code = django_filters.CharFilter(label='Directorate Code',lookup_expr='icontains')
    # directorate__directorate_name = django_filters.CharFilter(label='Directorate Name',lookup_expr='icontains')
    # cost_centre_code = django_filters.CharFilter(label='Cost Centre Code',lookup_expr='icontains')
    natural_account_code = django_filters.CharFilter(lookup_expr='istartswith')

    class Meta(MyFilterSet.Meta):
        model = NaturalCode
        fields = ['NAC_category', 'dashboard_grouping', 'natural_account_code', 'natural_account_code_description', ]
        exclude = ['used_by_DIT','account_L5_code']

    @property
    def qs(self):
        nac = super(NACFilter, self).qs
        return nac.filter(used_by_DIT=True)


