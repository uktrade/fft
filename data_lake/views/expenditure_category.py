from core.utils.generic_helpers import get_current_financial_year

from chartofaccountDIT.models import (
    ArchivedExpenditureCategory,
    ExpenditureCategory,
)

from data_lake.views.data_lake_view import DataLakeViewSet


class ExpenditureCategoryViewSet(DataLakeViewSet):
    filename = "budget_category"
    title_list = [
        "Budget Grouping",
        "Budget Category",
        "Description",
        "Further description",
        "Year",
    ]

    def write_data(self, writer):
        current_year = get_current_financial_year()
        current_queryset = ExpenditureCategory.objects.all().order_by(
            "-NAC_category__NAC_category_description",
            "grouping_description",
            "description",
            "further_description",
        )
        historical_queryset = (
            ArchivedExpenditureCategory.objects.all()
            .select_related("financial_year")
            .order_by(
                "-financial_year",
                "-NAC_category",
                "grouping_description",
                "description",
                "further_description",
            )
        )
        for obj in current_queryset:
            row = [
                obj.NAC_category.NAC_category_description,
                obj.grouping_description,
                obj.description,
                obj.further_description,
                current_year,
            ]
            writer.writerow(row)

        for obj in historical_queryset:
            row = [
                obj.NAC_category,
                obj.grouping_description,
                obj.description,
                obj.further_description,
                obj.financial_year.financial_year,
            ]
            writer.writerow(row)
