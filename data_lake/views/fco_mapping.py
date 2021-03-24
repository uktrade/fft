from core.utils.generic_helpers import get_current_financial_year

from chartofaccountDIT.models import (
    ArchivedFCOMapping,
    FCOMapping,
)

from data_lake.views.data_lake_view import DataLakeViewSet


class FCOMappingViewSet(DataLakeViewSet):
    filename = "fco_mapping"
    title_list = [
        "Expenditure Type",
        "Budget Grouping",
        "Budget Category",
        "DIT(Oracle) Code",
        "DIT(Oracle) Description",
        "FCO(Prism) Code",
        "FCO(Prism) Description",
        "Year",
    ]

    def write_data(self, writer):
        current_year = get_current_financial_year()
        current_queryset = (
            FCOMapping.objects.all()
            .select_related(
                "account_L6_code_fk",
                "account_L6_code_fk__expenditure_category",
                "account_L6_code_fk__expenditure_category__NAC_category",
            )
            .order_by(
                "account_L6_code_fk__economic_budget_code",
                "account_L6_code_fk__expenditure_category__NAC_category__NAC_category_description",  # noqa",
                "account_L6_code_fk__natural_account_code_description",
                "fco_code",
            )
        )
        historical_queryset = (
            ArchivedFCOMapping.objects.all()
            .select_related("financial_year")
            .order_by(
                "economic_budget_code",
                "nac_category_description",
                "account_L6_description",
                "fco_code",
            )
        )
        for obj in current_queryset:
            if obj.account_L6_code_fk.expenditure_category:
                expenditure_category_value = (
                    obj.expenditure_category.grouping_description
                )
                NAC_category_value = (
                    obj.expenditure_category.NAC_category.NAC_category_description
                )
            else:
                expenditure_category_value = None
                NAC_category_value = None

            row = [
                obj.account_L6_code_fk.economic_budget_code,
                NAC_category_value,
                expenditure_category_value,
                obj.account_L6_code_fk.natural_account_code,
                obj.account_L6_code_fk.natural_account_code_description,
                obj.fco_code,
                obj.fco_description,
                current_year,
            ]
            writer.writerow(row)

        for obj in historical_queryset:
            row = [
                obj.economic_budget_code,
                obj.nac_category_description,
                obj.budget_description,
                obj.account_L6_code,
                obj.account_L6_description,
                obj.fco_code,
                obj.fco_description,
                obj.financial_year.financial_year,
            ]
            writer.writerow(row)
