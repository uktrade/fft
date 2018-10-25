from core.filters import MyFilterSet

import django_filters

from .models import Analysis1, Analysis2, CommercialCategory, \
    ExpenditureCategory, NaturalCode, ProgrammeCode


class NACFilter(MyFilterSet):
    # natural_account_code = django_filters.CharFilter(lookup_expr='istartswith')
    account_L5_code__economic_budget_code = \
        django_filters.CharFilter(label='Expenditure Type', lookup_expr='icontains')

    class Meta(MyFilterSet.Meta):
        model = NaturalCode
        fields = ['account_L5_code__economic_budget_code',
                  'expenditure_category__NAC_category', 'expenditure_category',
                   'natural_account_code_description']
        exclude = ['active', 'account_L5_code']

    def __init__(self, *args, **kwargs):
        super(NACFilter, self).__init__(*args, **kwargs)
        self.filters['expenditure_category__NAC_category'].label = 'Budget Category'

    @property
    def qs(self):
        nac = super(NACFilter, self).qs
        return nac.filter(active=True).order_by('account_L5_code__economic_budget_code',
                                                'expenditure_category__NAC_category',
                                                'expenditure_category',
                                                'natural_account_code',
                                                'natural_account_code_description')


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


class Analysis1Filter(MyFilterSet):
    class Meta(MyFilterSet.Meta):
        model = Analysis1
        fields = ['analysis1_description']


class ProgrammeFilter(MyFilterSet):
    class Meta(MyFilterSet.Meta):
        model = ProgrammeCode
        fields = [
            'programme_code',
            'programme_description',
            'budget_type'
        ]

    @property
    def qs(self):
        prog = super(ProgrammeFilter, self).qs
        return prog.filter(active=True).order_by('programme_code',
                                                 'programme_description',
                                                 'budget_type')
