import django_filters

from core.filters import MyFilterSet
from .models import DepartmentalGroup, Directorate, CostCentre


class CostCentreFilter(MyFilterSet):
    directorate__group__group_code = django_filters.CharFilter(label='Group Code',lookup_expr='icontains')
    directorate__group__group_name = django_filters.CharFilter(label='Group Name',lookup_expr='icontains')
    directorate__directorate_code = django_filters.CharFilter(label='Directorate Code',lookup_expr='icontains')
    directorate__directorate_name = django_filters.CharFilter(label='Directorate Name',lookup_expr='icontains')
    # cost_centre_code = django_filters.CharFilter(label='Cost Centre Code',lookup_expr='icontains')
    # cost_centre_name = django_filters.CharFilter(label='Cost Centre Name',lookup_expr='icontains')

    class Meta:
        model = CostCentre
        fields = ['directorate__group__group_code',
                  'directorate__group__group_name',
                  'directorate__directorate_code',
                  'directorate__directorate_name',
                  'cost_centre_code',
                  'cost_centre_name']
        exclude = ['active','created','updated','directorate']

    @property
    def qs(self):
        cc = super(CostCentreFilter, self).qs
        return cc.filter(active=True)


