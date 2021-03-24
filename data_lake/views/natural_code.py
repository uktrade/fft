from core.utils.generic_helpers import get_current_financial_year

from chartofaccountDIT.models import (
    ArchivedNaturalCode,
    NaturalCode,
)

from data_lake.views.data_lake_view import DataLakeViewSet


class NaturalCodeViewSet(DataLakeViewSet):
    filename = "natural_account"
    title_list = [
        "Expenditure Type",
        "Budget Grouping",
        "Budget Category",
        "Commercial category",
        "Operational Delivery Plan",
        "Budget / Forecast NAC",
        "PO / Actuals NAC",
        "NAC Description",
        "Year",
    ]

    def write_data(self, writer):
        current_year = get_current_financial_year()
        current_queryset = (
            NaturalCode.objects.filter(active=True)
            .select_related("expenditure_category")
            .select_related("commercial_category")
            .order_by(
                "-economic_budget_code",
                "-expenditure_category__NAC_category__NAC_category_description",
                "-expenditure_category__grouping_description",
                "commercial_category__commercial_category",
                "natural_account_code",
            )
        )
        historical_queryset = (
            ArchivedNaturalCode.objects.filter(active=True)
            .select_related("financial_year")
            .order_by(
                "-financial_year",
                "-economic_budget_code",
                "-NAC_category",
                "-expenditure_category__grouping_description",
                "commercial_category",
                "natural_account_code",
            )
        )
        for obj in current_queryset:
            op_delivery_plan_value = None
            if obj.expenditure_category:
                expenditure_category_value = (
                    obj.expenditure_category.grouping_description
                )
                NAC_category_value = (
                    obj.expenditure_category.NAC_category.NAC_category_description
                )
                account_L6_budget_value = (
                    obj.expenditure_category.linked_budget_code.natural_account_code
                )
                if obj.expenditure_category.op_del_category:
                    op_delivery_plan_value = (
                        obj.expenditure_category.op_del_category.operating_delivery_description  # noqa E501
                    )
            else:
                expenditure_category_value = None
                NAC_category_value = None
                account_L6_budget_value = None

            if obj.commercial_category:
                commercial_category_value = obj.commercial_category.commercial_category
            else:
                commercial_category_value = ""

            row = [
                obj.economic_budget_code,
                NAC_category_value,
                expenditure_category_value,
                commercial_category_value,
                op_delivery_plan_value,
                account_L6_budget_value,
                obj.natural_account_code,
                obj.natural_account_code_description,
                current_year,
            ]
            writer.writerow(row)

        for obj in historical_queryset:
            row = [
                obj.economic_budget_code,
                obj.NAC_category,
                obj.expenditure_category_description,
                obj.commercial_category,
                obj.op_delivery_plan,
                obj.account_L6_budget,
                obj.natural_account_code,
                obj.natural_account_code_description,
                obj.financial_year.financial_year,
            ]
            writer.writerow(row)
