from core.filters import MyFilterSet

from django.db.models import Q

import django_filters

from .models import Analysis1, Analysis2, CommercialCategory, \
    ExpenditureCategory, FCOMapping, InterEntity, NaturalCode, ProgrammeCode, ProjectCode, \
    HistoricalProgrammeCode, HistoricalNaturalCode, HistoricalExpenditureCategory, HistoricalCommercialCategory, \
    HistoricalAnalysis2, HistoricalAnalysis1, HistoricalProjectCode, HistoricalFCOMapping, HistoricalInterEntity


class NACFilter(MyFilterSet):
    """It defines the filter for the NAC page. """
    search_all = django_filters.CharFilter(field_name='', label='',
                                           method='search_all_filter')

    def search_all_filter(selfself, queryset, name, value):
        return queryset.filter(Q(account_L5_code__economic_budget_code__icontains=value) |
                               Q(expenditure_category__NAC_category__NAC_category_description__icontains=value) |    # noqa: E501
                               Q(expenditure_category__linked_budget_code__natural_account_code__icontains=value) |    # noqa: E501
                               Q(expenditure_category__grouping_description__icontains=value) |
                               Q(commercial_category__commercial_category__icontains=value) |
                               Q(natural_account_code__icontains=value) |
                               Q(natural_account_code_description__icontains=value)
                               )

    class Meta(MyFilterSet.Meta):
        model = NaturalCode
        fields = ['search_all']

    @property
    def qs(self):
        myfilter = super(NACFilter, self).qs
        return myfilter.filter(active=True).select_related('expenditure_category'). \
            select_related('commercial_category').order_by('-account_L5_code__economic_budget_code',
                                                     '-expenditure_category__NAC_category__NAC_category_description',    # noqa: E501
                                                     '-expenditure_category__grouping_description',
                                                     'commercial_category__commercial_category',
                                                     'natural_account_code'
                                                     )


class HistoricalNACFilter(MyFilterSet):
    """Provide filter definition for Historical NAC. It cannot inherit from the current NAC filter class because the
    historical table is denormalised, and the fields are different."""
    search_all = django_filters.CharFilter(field_name='', label='',
                                           method='search_all_filter')

    def search_all_filter(selfself, queryset, name, value):
        return queryset.filter(Q(economic_budget_code__icontains=value) |
                               Q(NAC_category__icontains=value) |
                               Q(account_L6_budget__icontains=value) |
                               Q(expenditure_category__icontains=value) |
                               Q(commercial_category__icontains=value) |
                               Q(natural_account_code__icontains=value) |
                               Q(natural_account_code_description__icontains=value)
                               )

    class Meta(MyFilterSet.Meta):
        model = HistoricalNaturalCode
        fields = ['search_all']

    @property
    def qs(self):
        myfilter = super(HistoricalNACFilter, self).qs
        return myfilter.filter(active=True).order_by('-economic_budget_code',
                                                     '-NAC_category',
                                                     '-expenditure_category',
                                                     'commercial_category',
                                                     'natural_account_code'
                                                     )


class ExpenditureCategoryFilter(MyFilterSet):
    """It defines the filter for the Expenditure category page. """
    search_all = django_filters.CharFilter(field_name='', label='',
                                           method='search_all_filter')

    def search_all_filter(selfself, queryset, name, value):
        return queryset.filter(Q(NAC_category__NAC_category_description__icontains=value) |
                               Q(grouping_description__icontains=value) |
                               Q(description__icontains=value) |
                               Q(further_description__icontains=value)
                               )

    class Meta(MyFilterSet.Meta):
        model = ExpenditureCategory
        fields = ['search_all']

    @property
    def qs(self):
        # There is no Active field on the Expenditure Category table:
        # this is why there is no filter on Active  on the queryset
        myfilter = super(ExpenditureCategoryFilter, self).qs
        return myfilter.order_by('-NAC_category__NAC_category_description',
                                 'grouping_description',
                                 'description',
                                 'further_description')


class HistoricalExpenditureCategoryFilter(MyFilterSet):
    """Provide filter definition for Historical Expenditure Category.
    It cannot inherit from the current Historical Expenditure Category filter class because the
    historical table is denormalised, and the fields are different."""
    search_all = django_filters.CharFilter(field_name='', label='',
                                           method='search_all_filter')

    def search_all_filter(selfself, queryset, name, value):
        return queryset.filter(Q(NAC_category__icontains=value) |
                               Q(grouping_description__icontains=value) |
                               Q(description__icontains=value) |
                               Q(further_description__icontains=value)
                               )

    class Meta(MyFilterSet.Meta):
        model = HistoricalExpenditureCategory
        fields = ['search_all']

    @property
    def qs(self):
        # There is no Active field on the Expenditure Category table:
        # this is why there is no filter on Active  on the queryset
        myfilter = super(HistoricalExpenditureCategoryFilter, self).qs
        return myfilter.order_by('-NAC_category',
                                 'grouping_description',
                                 'description',
                                 'further_description')


class CommercialCategoryFilter(MyFilterSet):
    """Define the filter for the Commercial Category"""
    search_all = django_filters.CharFilter(field_name='', label='',
                                           method='search_all_filter')

    def search_all_filter(selfself, queryset, name, value):
        return queryset.filter(Q(commercial_category__icontains=value) |
                               Q(description__icontains=value))

    class Meta(MyFilterSet.Meta):
        model = CommercialCategory
        fields = ['search_all']

    @property
    def qs(self):
        # There is no Active field on the commercial Category table:
        # this is why there is no filter on Active  on the queryset
        myfilter = super(CommercialCategoryFilter, self).qs
        return myfilter.order_by('commercial_category',
                                 'description'
                                 )



class HistoricalCommercialCategoryFilter(CommercialCategoryFilter):
    """Provide the filter definition for Historical Commercial Category. Inherit from current one,
    because the fields are identical."""
    class Meta(CommercialCategoryFilter.Meta):
        model = HistoricalCommercialCategory



class Analysis1Filter(MyFilterSet):
    """Define the filter for  Analysis 1"""
    search_all = django_filters.CharFilter(field_name='', label='',
                                           method='search_all_filter')

    def search_all_filter(self, queryset, name, value):
        return queryset.filter(Q(analysis1_code__icontains=value) |
                               Q(analysis1_description__icontains=value) |
                               Q(supplier__icontains=value) |
                               Q(pc_reference__icontains=value)
                               )

    class Meta(MyFilterSet.Meta):
        model = Analysis1
        fields = ['search_all']

    @property
    def qs(self):
        myfilter = super(Analysis1Filter, self).qs
        return myfilter.filter(active=True).order_by('analysis1_code',
                                                     'analysis1_description'
                                                     )


class HistoricalAnalysis1Filter(Analysis1Filter):
    """Provide the filter definition for Analysis 2. Inherit from current one,
    because the fields are identical."""
    class Meta(Analysis1Filter.Meta):
        model = HistoricalAnalysis1



class Analysis2Filter(MyFilterSet):
    """Define the filter for Analysis 2 page"""
    search_all = django_filters.CharFilter(field_name='', label='',
                                           method='search_all_filter')

    def search_all_filter(self, queryset, name, value):
        return queryset.filter(Q(analysis2_code__icontains=value) |
                               Q(analysis2_description__icontains=value))

    class Meta(MyFilterSet.Meta):
        model = Analysis2
        fields = ['search_all']

    @property
    def qs(self):
        myfilter = super(Analysis2Filter, self).qs
        return myfilter.filter(active=True).order_by('analysis2_code',
                                                     'analysis2_description'
                                                     )


class HistoricalAnalysis2Filter(Analysis2Filter):
    """Provide the filter definition for Analysis 1. Inherit from current one,
    because the fields are identical."""
    class Meta(Analysis2Filter.Meta):
        model = HistoricalAnalysis2


class ProgrammeFilter(MyFilterSet):
    search_all = django_filters.CharFilter(field_name='', label='',
                                           method='search_all_filter')

    def search_all_filter(self, queryset, name, value):
        return queryset.filter(Q(programme_code__icontains=value) |
                               Q(programme_description__icontains=value) |
                               Q(budget_type__icontains=value)
                               )

    class Meta(MyFilterSet.Meta):
        model = ProgrammeCode
        fields = [
            'search_all',
        ]

    @property
    def qs(self):
        myfilter = super(ProgrammeFilter, self).qs
        return myfilter.filter(active=True).order_by('programme_code',
                                                     'programme_description',
                                                     'budget_type')


class HistoricalProgrammeFilter(ProgrammeFilter):
    """Provide the filter definition for Programme. Inherit from current one,
    because the fields are identical."""
    class Meta(ProgrammeFilter.Meta):
        model = HistoricalProgrammeCode


class InterEntityFilter(MyFilterSet):
    search_all = django_filters.CharFilter(field_name='', label='',
                                           method='search_all_filter')

    def search_all_filter(self, queryset, name, value):
        return queryset.filter(Q(l1_value__l1_description__icontains=value) |
                               Q(l1_value__l1_value__icontains=value) |
                               Q(l2_value__icontains=value) |
                               Q(l2_description__icontains=value) |
                               Q(cpid__icontains=value)
                               )

    class Meta(MyFilterSet.Meta):
        model = InterEntity
        fields = [
            'search_all',
        ]

    @property
    def qs(self):
        myfilter = super(InterEntityFilter, self).qs
        return myfilter.filter(active=True).order_by('l1_value__l1_value',
                                                     'l1_value__l1_description',
                                                     'l2_value'
                                                     )

class HistoricalInterEntityFilter(MyFilterSet):
    search_all = django_filters.CharFilter(field_name='', label='',
                                           method='search_all_filter')

    def search_all_filter(self, queryset, name, value):
        return queryset.filter(Q(l1_description__icontains=value) |
                               Q(l1_value__icontains=value) |
                               Q(l2_value__icontains=value) |
                               Q(l2_description__icontains=value) |
                               Q(cpid__icontains=value)
                               )

    class Meta(MyFilterSet.Meta):
        model = HistoricalInterEntity
        fields = [
            'search_all',
        ]

    @property
    def qs(self):
        myfilter = super(HistoricalInterEntityFilter, self).qs
        return myfilter.filter(active=True).order_by('l1_value',
                                                     'l1_description',
                                                     'l2_value'
                                                     )


class ProjectFilter(MyFilterSet):
    search_all = django_filters.CharFilter(field_name='', label='',
                                           method='search_all_filter')

    def search_all_filter(self, queryset, name, value):
        return queryset.filter(Q(project_code__icontains=value) |
                               Q(project_description__icontains=value))

    class Meta(MyFilterSet.Meta):
        model = ProjectCode
        fields = ['search_all']

    @property
    def qs(self):
        myfilter = super(ProjectFilter, self).qs
        return myfilter.filter(active=True).order_by('project_code')


class HistoricalProjectFilter(ProjectFilter):
    """Provide the filter definition for Programme. Inherit from current one,
    because the fields are identical."""

    class Meta(ProjectFilter.Meta):
        model = HistoricalProjectCode


class FCOMappingtFilter(MyFilterSet):
    search_all = django_filters.CharFilter(field_name='', label='',
                                           method='search_all_filter')

    def search_all_filter(self, queryset, name, value):
        return queryset.filter(Q(fco_code__icontains=value) |
                               Q(fco_description__icontains=value) |
                               Q(account_L6_code_fk__natural_account_code__icontains=value) |
                               Q(account_L6_code_fk__natural_account_code_description__icontains=value) |
                               Q(account_L6_code_fk__expenditure_category__NAC_category__NAC_category_description__icontains=value) |
                               Q(account_L6_code_fk__expenditure_category__grouping_description__icontains=value) |
                               Q(account_L6_code_fk__account_L5_code__economic_budget_code__icontains=value)
                               )

    class Meta(MyFilterSet.Meta):
        model = FCOMapping
        fields = ['search_all']

    @property
    def qs(self):
        myfilter = super(FCOMappingtFilter, self).qs
        return myfilter.filter(active=True).order_by('fco_code')


class HistoricalFCOMappingtFilter(MyFilterSet):
    search_all = django_filters.CharFilter(field_name='', label='',
                                           method='search_all_filter')

    def search_all_filter(self, queryset, name, value):
        return queryset.filter(Q(fco_code__icontains=value) |
                               Q(fco_description__icontains=value) |
                               Q(account_L6_code__icontains=value) |
                               Q(account_L6_description__icontains=value) |
                               Q(nac_category_description__icontains=value) |
                               Q(budget_description__icontains=value) |
                               Q(economic_budget_code__icontains=value)
                               )

    class Meta(MyFilterSet.Meta):
        model = HistoricalFCOMapping
        fields = ['search_all']

    @property
    def qs(self):
        myfilter = super(HistoricalFCOMappingtFilter, self).qs
        return myfilter.filter(active=True).order_by('fco_code')


