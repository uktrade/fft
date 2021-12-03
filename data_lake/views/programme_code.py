from core.utils.generic_helpers import get_current_financial_year

from chartofaccountDIT.models import (
    ArchivedProgrammeCode,
    ProgrammeCode,
)

from data_lake.views.data_lake_view import DataLakeViewSet


class ProgrammeCodeViewSet(DataLakeViewSet):
    filename = "programme_code"
    title_list = [
        "Programme Code",
        "Programme Name",
        "Budget Type",
        "Budget Type Display",
        "Year",
    ]

    def write_data(self, writer):
        current_year = get_current_financial_year()
        current_queryset = ProgrammeCode.objects.filter(active=True).order_by(
            "programme_code", "programme_description", "budget_type__budget_type"
        )
        historical_queryset = (
            ArchivedProgrammeCode.objects.filter(active=True)
            .select_related("financial_year")
            .order_by(
                "-financial_year",
                "programme_code",
                "programme_description",
                "budget_type__budget_type",
            )
        )

        for obj in current_queryset:
            if obj.budget_type:
                budget_type = obj.budget_type.budget_type
                budget_type_display = obj.budget_type.budget_type_display
            else:
                budget_type = None
                budget_type_display = None

            row = [
                obj.programme_code,
                obj.programme_description,
                budget_type,
                budget_type_display,
                current_year,
            ]
            writer.writerow(row)

        for obj in historical_queryset:
            if obj.budget_type:
                budget_type = obj.budget_type.budget_type
                budget_type_display = obj.budget_type.budget_type_display
            else:
                budget_type = None
                budget_type_display = None
            row = [
                obj.programme_code,
                obj.programme_description,
                budget_type,
                budget_type_display,
                obj.financial_year.financial_year,
            ]
            writer.writerow(row)
