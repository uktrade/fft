from django.db.models import Q

import django_filters

from chartofaccountDIT.models import (
    Analysis1,
    Analysis2,
    ArchivedAnalysis1,
    ArchivedAnalysis2,
    ArchivedCommercialCategory,
    ArchivedExpenditureCategory,
    ArchivedFCOMapping,
    ArchivedInterEntity,
    ArchivedNaturalCode,
    ArchivedProgrammeCode,
    ArchivedProjectCode,
    CommercialCategory,
    ExpenditureCategory,
    FCOMapping,
    InterEntity,
    NaturalCode,
    ProgrammeCode,
    ProjectCode,
)

from core.filters import (ArchivedFilterSet,
                          MyFilterSet,
                          )


class NACFilter(MyFilterSet):
    """It defines the filter for the NAC page. """

    search_all = django_filters.CharFilter(
        field_name="", label="", method="search_all_filter"
    )

    def search_all_filter(selfself, queryset, name, value):
        return queryset.filter(
            Q(economic_budget_code__icontains=value)
            | Q(
                expenditure_category__NAC_category__NAC_category_description__icontains=value  # noqa
            )
            | Q(  # noqa: E501
                expenditure_category__op_del_category__operating_delivery_description__icontains=value  # noqa
            )
            | Q(  # noqa: E501
                expenditure_category__linked_budget_code__natural_account_code__icontains=value  # noqa
            )
            | Q(  # noqa: E501
                expenditure_category__grouping_description__icontains=value  # noqa
            )
            | Q(commercial_category__commercial_category__icontains=value)
            | Q(natural_account_code__icontains=value)
            | Q(natural_account_code_description__icontains=value)
        )

    class Meta(MyFilterSet.Meta):
        model = NaturalCode
        fields = ["search_all"]

    @property
    def qs(self):
        my_filter = super(NACFilter, self).qs
        return (
            my_filter.filter(active=True)
            .select_related("expenditure_category")
            .select_related("commercial_category")
            .order_by(
                "-economic_budget_code",
                "-expenditure_category__NAC_category__NAC_category_description",
                # noqa: E501
                "-expenditure_category__grouping_description",
                "commercial_category__commercial_category",
                "natural_account_code",
            )
        )


class HistoricalNACFilter(ArchivedFilterSet):
    """Provide filter definition for
    Historical NAC. It cannot inherit
    from the current NAC filter class
    because the historical table is
    denormalised, and the fields are
    different."""

    search_all = django_filters.CharFilter(
        field_name="", label="", method="search_all_filter"
    )

    def search_all_filter(selfself, queryset, name, value):
        return queryset.filter(
            Q(economic_budget_code__icontains=value)
            | Q(NAC_category__icontains=value)
            | Q(account_L6_budget__icontains=value)
            | Q(expenditure_category__grouping_description__icontains=value)
            | Q(commercial_category__icontains=value)
            | Q(natural_account_code__icontains=value)
            | Q(natural_account_code_description__icontains=value)
        )

    class Meta(ArchivedFilterSet.Meta):
        model = ArchivedNaturalCode
        fields = ["search_all"]

    @property
    def qs(self):
        qs_filtered = super(HistoricalNACFilter, self).qs
        return qs_filtered.filter(active=True).order_by(
            "-economic_budget_code",
            "-NAC_category",
            "-expenditure_category__grouping_description",
            "commercial_category",
            "natural_account_code",
        )


class ExpenditureCategoryFilter(MyFilterSet):
    """It defines the filter for the Expenditure category page. """

    search_all = django_filters.CharFilter(
        field_name="", label="", method="search_all_filter"
    )

    def search_all_filter(selfself, queryset, name, value):
        return queryset.filter(
            Q(NAC_category__NAC_category_description__icontains=value)
            | Q(grouping_description__icontains=value)
            | Q(description__icontains=value)
            | Q(further_description__icontains=value)
        )

    class Meta(MyFilterSet.Meta):
        model = ExpenditureCategory
        fields = ["search_all"]

    @property
    def qs(self):
        # There is no Active field on the Expenditure Category table:
        # this is why there is no filter on Active  on the queryset
        qs_filtered = super(ExpenditureCategoryFilter, self).qs
        return qs_filtered.order_by(
            "-NAC_category__NAC_category_description",
            "grouping_description",
            "description",
            "further_description",
        )


class HistoricalExpenditureCategoryFilter(ArchivedFilterSet):
    """Provide filter definition for
    Historical Expenditure Category.
    It cannot inherit from the current
    Historical Expenditure Category
    filter class because the historical
    table is denormalised, and the
    fields are different."""

    search_all = django_filters.CharFilter(
        field_name="", label="", method="search_all_filter"
    )

    def search_all_filter(selfself, queryset, name, value):
        return queryset.filter(
            Q(NAC_category_description__icontains=value)
            | Q(grouping_description__icontains=value)
            | Q(description__icontains=value)
            | Q(further_description__icontains=value)
        )

    class Meta(ArchivedFilterSet.Meta):
        model = ArchivedExpenditureCategory
        fields = ["search_all"]

    @property
    def qs(self):
        # There is no Active field on the Expenditure Category table:
        # this is why there is no filter on Active  on the queryset
        qs_filtered = super(HistoricalExpenditureCategoryFilter, self).qs
        return qs_filtered.order_by(
            "-NAC_category",
            "grouping_description",
            "description",
            "further_description",
        )


class CommercialCategoryFilter(MyFilterSet):
    """Define the filter for the Commercial Category"""

    search_all = django_filters.CharFilter(
        field_name="", label="", method="search_all_filter"
    )

    def search_all_filter(selfself, queryset, name, value):
        return queryset.filter(
            Q(commercial_category__icontains=value) | Q(description__icontains=value)
        )

    class Meta(MyFilterSet.Meta):
        model = CommercialCategory
        fields = ["search_all"]

    @property
    def qs(self):
        # There is no Active field on the commercial Category table:
        # this is why there is no filter on Active  on the queryset
        qs_filtered = super(CommercialCategoryFilter, self).qs
        return qs_filtered.order_by("commercial_category", "description")


class HistoricalCommercialCategoryFilter(ArchivedFilterSet):
    search_all = django_filters.CharFilter(
        field_name="", label="", method="search_all_filter"
    )

    def search_all_filter(selfself, queryset, name, value):
        return queryset.filter(
            Q(commercial_category__icontains=value) | Q(description__icontains=value)
        )

    class Meta(ArchivedFilterSet.Meta):
        model = ArchivedCommercialCategory
        fields = ["search_all"]

    @property
    def qs(self):
        # There is no Active field on the commercial Category table:
        # this is why there is no filter on Active  on the queryset
        qs_filtered = super(HistoricalCommercialCategoryFilter, self).qs
        return qs_filtered.order_by("commercial_category", "description")


class Analysis1Filter(MyFilterSet):
    """Define the filter for  Analysis 1"""

    search_all = django_filters.CharFilter(
        field_name="", label="", method="search_all_filter"
    )

    def search_all_filter(self, queryset, name, value):
        return queryset.filter(
            Q(analysis1_code__icontains=value)
            | Q(analysis1_description__icontains=value)
            | Q(supplier__icontains=value)
            | Q(pc_reference__icontains=value)
        )

    class Meta(MyFilterSet.Meta):
        model = Analysis1
        fields = ["search_all"]

    @property
    def qs(self):
        qs_filtered = super(Analysis1Filter, self).qs
        return qs_filtered.filter(active=True).order_by(
            "analysis1_code", "analysis1_description"
        )


class HistoricalAnalysis1Filter(ArchivedFilterSet):
    search_all = django_filters.CharFilter(
        field_name="", label="", method="search_all_filter"
    )

    def search_all_filter(self, queryset, name, value):
        return queryset.filter(
            Q(analysis1_code__icontains=value)
            | Q(analysis1_description__icontains=value)
            | Q(supplier__icontains=value)
            | Q(pc_reference__icontains=value)
        )

    class Meta(ArchivedFilterSet.Meta):
        model = ArchivedAnalysis1
        fields = ["search_all"]

    @property
    def qs(self):
        qs_filtered = super(HistoricalAnalysis1Filter, self).qs
        return qs_filtered.filter(active=True).order_by(
            "analysis1_code", "analysis1_description"
        )


class Analysis2Filter(MyFilterSet):
    """Define the filter for Analysis 2 page"""

    search_all = django_filters.CharFilter(
        field_name="", label="", method="search_all_filter"
    )

    def search_all_filter(self, queryset, name, value):
        return queryset.filter(
            Q(analysis2_code__icontains=value)
            | Q(analysis2_description__icontains=value)
        )

    class Meta(MyFilterSet.Meta):
        model = Analysis2
        fields = ["search_all"]

    @property
    def qs(self):
        qs_filtered = super(Analysis2Filter, self).qs
        return qs_filtered.filter(active=True).order_by(
            "analysis2_code", "analysis2_description"
        )


class HistoricalAnalysis2Filter(ArchivedFilterSet):
    search_all = django_filters.CharFilter(
        field_name="", label="", method="search_all_filter"
    )

    def search_all_filter(self, queryset, name, value):
        return queryset.filter(
            Q(analysis2_code__icontains=value)
            | Q(analysis2_description__icontains=value)
        )

    class Meta(ArchivedFilterSet.Meta):
        model = ArchivedAnalysis2
        fields = ["search_all"]

    @property
    def qs(self):
        qs_filtered = super(HistoricalAnalysis2Filter, self).qs
        return qs_filtered.filter(active=True).order_by(
            "analysis2_code", "analysis2_description"
        )


class ProgrammeFilter(MyFilterSet):
    search_all = django_filters.CharFilter(
        field_name="", label="", method="search_all_filter"
    )

    def search_all_filter(self, queryset, name, value):
        return queryset.filter(
            Q(programme_code__icontains=value)
            | Q(programme_description__icontains=value)
            | Q(budget_type__budget_type__icontains=value)
        )

    class Meta(MyFilterSet.Meta):
        model = ProgrammeCode
        fields = ["search_all"]

    @property
    def qs(self):
        qs_filtered = super(ProgrammeFilter, self).qs
        return qs_filtered.filter(active=True).order_by(
            "programme_code", "programme_description", "budget_type__budget_type"
        )


class HistoricalProgrammeFilter(ArchivedFilterSet, ProgrammeFilter):
    class Meta(ArchivedFilterSet.Meta):
        model = ArchivedProgrammeCode
        fields = ["search_all"]


class InterEntityFilter(MyFilterSet):
    search_all = django_filters.CharFilter(
        field_name="", label="", method="search_all_filter"
    )

    def search_all_filter(self, queryset, name, value):
        return queryset.filter(
            Q(l1_value__l1_description__icontains=value)
            | Q(l1_value__l1_value__icontains=value)
            | Q(l2_value__icontains=value)
            | Q(l2_description__icontains=value)
            | Q(cpid__icontains=value)
        )

    class Meta(MyFilterSet.Meta):
        model = InterEntity
        fields = ["search_all"]

    @property
    def qs(self):
        qs_filtered = super(InterEntityFilter, self).qs
        return qs_filtered.filter(active=True).order_by(
            "l1_value__l1_value", "l1_value__l1_description", "l2_value"
        )


class HistoricalInterEntityFilter(ArchivedFilterSet):
    search_all = django_filters.CharFilter(
        field_name="", label="", method="search_all_filter"
    )

    def search_all_filter(self, queryset, name, value):
        return queryset.filter(
            Q(l1_description__icontains=value)
            | Q(l1_value__icontains=value)
            | Q(l2_value__icontains=value)
            | Q(l2_description__icontains=value)
            | Q(cpid__icontains=value)
        )

    class Meta(ArchivedFilterSet.Meta):
        model = ArchivedInterEntity
        fields = ["search_all"]

    @property
    def qs(self):
        qs_filtered = super(HistoricalInterEntityFilter, self).qs
        return qs_filtered.filter(active=True).order_by(
            "l1_value", "l1_description", "l2_value"
        )


class ProjectFilter(MyFilterSet):
    search_all = django_filters.CharFilter(
        field_name="", label="", method="search_all_filter"
    )

    def search_all_filter(self, queryset, name, value):
        return queryset.filter(
            Q(project_code__icontains=value)
            | Q(project_description__icontains=value)
        )

    class Meta(MyFilterSet.Meta):
        model = ProjectCode
        fields = ["search_all"]

    @property
    def qs(self):
        qs_filtered = super(ProjectFilter, self).qs
        return qs_filtered.filter(active=True).order_by("project_code")


class HistoricalProjectFilter(ArchivedFilterSet):
    search_all = django_filters.CharFilter(
        field_name="", label="", method="search_all_filter"
    )

    def search_all_filter(self, queryset, name, value):
        return queryset.filter(
            Q(project_code__icontains=value)
            | Q(project_description__icontains=value)
        )

    class Meta(ArchivedFilterSet.Meta):
        model = ArchivedProjectCode
        fields = ["search_all"]

    @property
    def qs(self):
        qs_filtered = super(HistoricalProjectFilter, self).qs
        return qs_filtered.filter(active=True).order_by("project_code")


class FCOMappingtFilter(MyFilterSet):
    search_all = django_filters.CharFilter(
        field_name="", label="", method="search_all_filter"
    )

    def search_all_filter(self, queryset, name, value):
        return queryset.filter(
            Q(fco_code__icontains=value)
            | Q(fco_description__icontains=value)
            | Q(account_L6_code_fk__natural_account_code__icontains=value)
            | Q(account_L6_code_fk__natural_account_code_description__icontains=value)
            | Q(account_L6_code_fk__expenditure_category__NAC_category__NAC_category_description__icontains=value)# noqa
            | Q(account_L6_code_fk__expenditure_category__grouping_description__icontains=value)  # noqa
            | Q(account_L6_code_fk__economic_budget_code__icontains=value)  # noqa
        )

    class Meta(MyFilterSet.Meta):
        model = FCOMapping
        fields = ["search_all"]

    @property
    def qs(self):
        qs_filtered = super(FCOMappingtFilter, self).qs
        return qs_filtered.filter(active=True).order_by("fco_code")


class HistoricalFCOMappingtFilter(ArchivedFilterSet):
    search_all = django_filters.CharFilter(
        field_name="", label="", method="search_all_filter"
    )

    def search_all_filter(self, queryset, name, value):
        return queryset.filter(
            Q(fco_code__icontains=value)
            | Q(fco_description__icontains=value)
            | Q(account_L6_code__icontains=value)
            | Q(account_L6_description__icontains=value)
            | Q(nac_category_description__icontains=value)
            | Q(budget_description__icontains=value)
            | Q(economic_budget_code__icontains=value)
        )

    class Meta(ArchivedFilterSet.Meta):
        model = ArchivedFCOMapping
        fields = ["search_all"]

    @property
    def qs(self):
        qs_filtered = super(HistoricalFCOMappingtFilter, self).qs
        return qs_filtered.filter(active=True).order_by("fco_code")
