from core.utils.generic_helpers import get_current_financial_year

from chartofaccountDIT.models import (
    ArchivedInterEntity,
    InterEntity,
)

from data_lake.views.data_lake_view import DataLakeViewSet


class InterEntityViewSet(DataLakeViewSet):
    filename = "inter_entity"
    title_list = [
        "L1 Value",
        "L1 Description",
        "ORACLE - Inter Entity Code",
        "ORACLE - Inter Entity Description",
        "Treasury - CPID(Departmental Code No.) ",
        "Year",
    ]

    def write_data(self, writer):
        current_year = get_current_financial_year()
        current_queryset = (
            InterEntity.objects.filter(active=True)
            .select_related("l1_value")
            .order_by("l1_value__l1_value", "l1_value__l1_description", "l2_value")
        )
        historical_queryset = (
            ArchivedInterEntity.objects.filter(active=True)
            .select_related("financial_year")
            .order_by("-financial_year", "l1_value", "l1_description", "l2_value",)
        )
        for obj in current_queryset:
            row = [
                obj.l1_value.l1_value,
                obj.l1_value.l1_description,
                obj.l2_value,
                obj.l2_description,
                obj.cpid,
                current_year,
            ]
            writer.writerow(row)

        for obj in historical_queryset:
            row = [
                obj.l1_value,
                obj.l1_description,
                obj.l2_value,
                obj.l2_description,
                obj.cpid,
                obj.financial_year.financial_year,
            ]
            writer.writerow(row)
