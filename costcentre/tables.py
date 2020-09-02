import django_tables2 as tables

from core.tables import FadminTable

from costcentre.models import (
    ArchivedCostCentre,
    CostCentre,
)


class CostCentreTable(FadminTable):
    group_code = tables.Column(
        verbose_name="Group No.", accessor="directorate.group.group_code"
    )
    directorate_code = tables.Column(
        verbose_name="Directorate No.", accessor="directorate.directorate_code"
    )
    group_name = tables.Column(
        verbose_name="Group Name", accessor="directorate.group.group_name"
    )
    directorate_name = tables.Column(
        verbose_name="Directorate Name", accessor="directorate.directorate_name"
    )
    director_general = tables.Column(
        verbose_name="Director General", accessor="directorate.group.director_general"
    )
    director = tables.Column(verbose_name="Director", accessor="directorate.director")

    class Meta(FadminTable.Meta):
        model = CostCentre
        fields = (
            "group_code",
            "group_name",
            "directorate_code",
            "directorate_name",
            "cost_centre_code",
            "cost_centre_name",
            "director",
            "director_general",
            "business_partner",
            "bsce_email",
        )


class HistoricalCostCentreTable(FadminTable):
    class Meta(FadminTable.Meta):
        model = ArchivedCostCentre
        fields = (
            "group_code",
            "group_name",
            "directorate_code",
            "directorate_name",
            "cost_centre_code",
            "cost_centre_name",
            "director_fullname",
            "dg_fullname",
            "business_partner_fullname",
            "bsce_email",
        )
