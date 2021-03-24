from core.utils.generic_helpers import get_current_financial_year

from chartofaccountDIT.models import (
    CommercialCategory,
    ArchivedCommercialCategory,
)

from data_lake.views.data_lake_view import DataLakeViewSet


class CommercialCategoryViewSet(DataLakeViewSet):
    filename = "commercial_category"
    title_list = [
        "Commercial Category",
        "Description",
        "Year",
    ]

    def write_data(self, writer):
        current_year = get_current_financial_year()
        current_queryset = CommercialCategory.objects.filter(active=True).order_by(
            "commercial_category",
        )
        historical_queryset = (
            ArchivedCommercialCategory.objects.filter(active=True)
            .select_related("financial_year")
            .order_by("-financial_year", "commercial_category")
        )
        for obj in current_queryset:
            row = [
                obj.commercial_category,
                obj.description,
                current_year,
            ]
            writer.writerow(row)

        for obj in historical_queryset:
            row = [
                obj.commercial_category,
                obj.description,
                obj.financial_year.financial_year,
            ]
            writer.writerow(row)
