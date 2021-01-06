from core.utils.generic_helpers import get_current_financial_year

from chartofaccountDIT.models import (
    ArchivedProjectCode,
    ProjectCode,
)

from data_lake.views.data_lake_view import DataLakeViewSet


class ProjectCodeViewSet(DataLakeViewSet,):
    filename = "project_code"
    title_list = [
        "Project Code",
        "Project Description",
        "Year",
    ]

    def write_data(self, writer):
        current_year = get_current_financial_year()
        current_queryset = ProjectCode.objects.filter(active=True).order_by(
            "project_code",
        )
        historical_queryset = (
            ArchivedProjectCode.objects.filter(active=True)
            .select_related("financial_year")
            .order_by("-financial_year", "project_code",)
        )
        for obj in current_queryset:
            row = [
                obj.project_code,
                obj.project_description,
                current_year,
            ]
            writer.writerow(row)

        for obj in historical_queryset:
            row = [
                obj.project_code,
                obj.project_description,
                obj.financial_year.financial_year,
            ]
            writer.writerow(row)
