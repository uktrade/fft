from django.db.models import Q

import django_filters

from core.filters import ArchivedFilterSet, MyFilterSet

from costcentre.models import (
    CostCentre,
    HistoricCostCentre,
)


class CostCentreFilter(MyFilterSet):
    """Use a single text box to enter an object name.
    It will search into group, directorate and cost centre name
    """

    search_all = django_filters.CharFilter(
        field_name="", label="", method="search_all_filter"
    )

    def search_all_filter(self, queryset, name, value):
        return queryset.filter(
            Q(directorate__group__group_name__icontains=value)
            | Q(directorate__directorate_name__icontains=value)
            | Q(cost_centre_name__icontains=value)
            | Q(directorate__group__group_code__icontains=value)
            | Q(directorate__directorate_code__icontains=value)
            | Q(cost_centre_code__icontains=value)
            | Q(directorate__group__director_general__name__icontains=value)
            | Q(directorate__group__director_general__surname__icontains=value)
            | Q(directorate__director__name__icontains=value)
            | Q(directorate__director__surname__icontains=value)
            | Q(business_partner__name__icontains=value)
            | Q(business_partner__surname__icontains=value)
        )

    class Meta(MyFilterSet.Meta):
        model = CostCentre
        fields = ["search_all"]

    @property
    def qs(self):
        cc = super(CostCentreFilter, self).qs
        return (
            cc.filter(active=True)
            .select_related("directorate")
            .select_related("deputy_director")
            .select_related("directorate__group")
            .order_by(
                "directorate__group__group_code",
                "directorate__group__group_name",
                "directorate__directorate_code",
                "directorate__directorate_name",
                "cost_centre_code",
            )
        )


class CostCentreHistoricalFilter(ArchivedFilterSet):
    """Use a single text box to enter an object name.
    It will search into group, directorate and cost centre name
    """

    search_all = django_filters.CharFilter(
        field_name="", label="", method="search_all_filter"
    )
    year = 0

    def search_all_filter(self, queryset, name, value):
        return queryset.filter(
            Q(group_name__icontains=value)
            | Q(directorate_name__icontains=value)
            | Q(cost_centre_name__icontains=value)
            | Q(group_code__icontains=value)
            | Q(directorate_code__icontains=value)
            | Q(cost_centre_code__icontains=value)
            | Q(dg_fullname__icontains=value)
            | Q(director_fullname__icontains=value)
            | Q(business_partner_fullname__icontains=value)
        )

    class Meta(MyFilterSet.Meta):
        model = HistoricCostCentre
        fields = ["search_all"]

    @property
    def qs(self):
        cc = super(CostCentreHistoricalFilter, self).qs.filter(financial_year=self.year)
        return cc.filter(active=True).order_by(
            "group_code",
            "group_name",
            "directorate_code",
            "directorate_name",
            "cost_centre_code",
        )
