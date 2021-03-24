from core.utils.generic_helpers import get_current_financial_year

from chartofaccountDIT.models import (
    Analysis1,
    ArchivedAnalysis1,
)

from data_lake.views.data_lake_view import DataLakeViewSet


class Analysis1CodeViewSet(DataLakeViewSet):
    filename = "contract_code"
    title_list = [
        "Contract Code",
        "Contract Name",
        "Supplier",
        "PC Reference",
        "Year",
    ]

    def write_data(self, writer):
        current_year = get_current_financial_year()
        current_queryset = Analysis1.objects.filter(active=True).order_by(
            "analysis1_code", "analysis1_description",
        )
        historical_queryset = (
            ArchivedAnalysis1.objects.filter(active=True)
            .select_related("financial_year")
            .order_by("-financial_year", "analysis1_code", "analysis1_description",)
        )
        for obj in current_queryset:
            row = [
                obj.analysis1_code,
                obj.analysis1_description,
                obj.supplier,
                obj.pc_reference,
                current_year,
            ]
            writer.writerow(row)

        for obj in historical_queryset:
            row = [
                obj.analysis1_code,
                obj.analysis1_description,
                obj.supplier,
                obj.pc_reference,
                obj.financial_year.financial_year,
            ]
            writer.writerow(row)
