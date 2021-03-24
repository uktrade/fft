from core.utils.generic_helpers import get_current_financial_year

from costcentre.models import (
    ArchivedCostCentre,
    CostCentre,
)

from data_lake.views.data_lake_view import DataLakeViewSet


class HierarchyViewSet(DataLakeViewSet):
    filename = "hierarchy"
    title_list = [
        "Group No.",
        "Group Name",
        "Directorate No.",
        "Directorate Name",
        "Cost Centre Code",
        "Cost Centre Name",
        "Director",
        "Director General",
        "Finance Business Partner",
        "BSCE Email",
        "Year",
    ]

    def write_data(self, writer):
        current_year = get_current_financial_year()
        current_queryset = (
            CostCentre.objects.filter(active=True)
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
        historical_queryset = (
            ArchivedCostCentre.objects.filter(active=True)
            .select_related("financial_year")
            .order_by(
                "-financial_year",
                "group_code",
                "group_name",
                "directorate_code",
                "directorate_name",
                "cost_centre_code",
            )
        )
        for obj in current_queryset:
            row = [
                obj.directorate.group.group_code,
                obj.directorate.group.group_name,
                obj.directorate.directorate_code,
                obj.directorate.directorate_name,
                obj.cost_centre_code,
                obj.cost_centre_name,
                obj.directorate.director,
                obj.directorate.group.director_general,
                obj.business_partner,
                obj.bsce_email,
                current_year,
            ]
            writer.writerow(row)

        for obj in historical_queryset:
            row = [
                obj.group_code,
                obj.group_name,
                obj.directorate_code,
                obj.directorate_name,
                obj.cost_centre_code,
                obj.cost_centre_name,
                obj.director_fullname,
                obj.dg_fullname,
                obj.business_partner_fullname,
                obj.bsce_email,
                obj.financial_year.financial_year,
            ]
            writer.writerow(row)
