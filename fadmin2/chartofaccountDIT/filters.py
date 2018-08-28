import django_filters
from .models import  NaturalCode, Analysis1, Analysis2, ExpenditureCategory, CommercialCategory
from core.filters import MyFilterSet


class NACFilter(MyFilterSet):
    natural_account_code = django_filters.CharFilter(lookup_expr='istartswith')
    account_L5_code__economic_budget_code = django_filters.CharFilter(label='Expenditure Type', lookup_expr='icontains')
    class Meta(MyFilterSet.Meta):
        model = NaturalCode
        fields = ['account_L5_code__economic_budget_code', 'expenditure_category__NAC_category', 'expenditure_category', 'natural_account_code', 'natural_account_code_description']
        exclude = ['used_by_DIT','account_L5_code']

    def __init__(self, *args, **kwargs):
        super(NACFilter, self).__init__(*args, **kwargs)
        self.filters['expenditure_category__NAC_category'].label = 'Budget Category'

    @property
    def qs(self):
        nac = super(NACFilter, self).qs
        return nac.filter(used_by_DIT=True)


class ExpenditureCategoryFilter(MyFilterSet):
    class Meta(MyFilterSet.Meta):
        model = ExpenditureCategory
        fields = ['NAC_category']


class CommercialCategoryFilter(MyFilterSet):
    class Meta(MyFilterSet.Meta):
        model = CommercialCategory
        fields = ['description']


class Analysis2Filter(MyFilterSet):
    class Meta(MyFilterSet.Meta):
        model = Analysis2
        fields = ['analysis2_description']

