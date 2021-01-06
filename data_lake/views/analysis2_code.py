from core.utils.generic_helpers import get_current_financial_year

from chartofaccountDIT.models import (
    Analysis2,
    ArchivedAnalysis2,
)

from data_lake.views.data_lake_view import DataLakeViewSet


class Analysis2CodeViewSet(DataLakeViewSet,):
    filename = "market_code"
    title_list = [
        "Market Code",
        "Market",
        "Year",
    ]

    def write_data(self, writer):
        current_year = get_current_financial_year()
        current_queryset = Analysis2.objects.filter(active=True).order_by(
            "analysis2_code", "analysis2_description",
        )
        historical_queryset = (
            ArchivedAnalysis2.objects.filter(active=True)
            .select_related("financial_year")
            .order_by("-financial_year", "analysis2_code", "analysis2_description",)
        )
        for obj in current_queryset:
            row = [
                obj.analysis2_code,
                obj.analysis2_description,
                current_year,
            ]
            writer.writerow(row)

        for obj in historical_queryset:
            row = [
                obj.analysis2_code,
                obj.analysis2_description,
                obj.financial_year.financial_year,
            ]
            writer.writerow(row)
