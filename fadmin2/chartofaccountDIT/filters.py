import django_filters
from .models import NACCategory, NaturalCode, Analysis1, Analysis2, NACDashboardGrouping
from core.filters import MyFilterSet


class NACFilter(MyFilterSet):
    natural_account_code = django_filters.CharFilter(lookup_expr='istartswith')
    account_L5_code__economic_budget_code = django_filters.CharFilter(label='Expenditure Type', lookup_expr='icontains')
    class Meta(MyFilterSet.Meta):
        model = NaturalCode
        fields = ['account_L5_code__economic_budget_code', 'NAC_category', 'dashboard_grouping', 'natural_account_code', 'natural_account_code_description']
        exclude = ['used_by_DIT','account_L5_code']

    @property
    def qs(self):
        nac = super(NACFilter, self).qs
        return nac.filter(used_by_DIT=True)


