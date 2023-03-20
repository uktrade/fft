from django.db.models import ExpressionWrapper, IntegerField, Value
from django.db.models.functions import Coalesce

from core.utils.generic_helpers import get_current_financial_year
from data_lake.views.utils import FigureFieldData
from end_of_month.models import EndOfMonthStatus


ARCHIVED_PERIOD_0_NAME = "Period 0"


class MIReportFieldList(FigureFieldData):
    filter_on_archived_period = False
    exclude_adj_period = True

    def write_queryset_data(self, writer, queryset):
        # Apply the filters and annotations common to  the budget, forecast and actual
        # data feed
        #
        current_year = get_current_financial_year()
        self.set_fields()
        # Change the list of fields, to use the field showing 0 instead of null
        market_field = "market"
        contract_field = "contract"
        project_field = "project"
        self.chart_of_account_field_list = [
            self.cost_centre_field,
            self.nac_field,
            self.programme_field,
            contract_field,
            market_field,
            project_field,
            self.expenditure_type_field,
            self.expenditure_type_description_field,
        ]

        filter_dict = {}
        if self.filter_on_archived_period:
            # Download all the archived period.
            max_period_id = (
                EndOfMonthStatus.archived_period_objects.get_latest_archived_period()
            )
            filter_dict["archived_period__lte"] = max_period_id

        if self.exclude_adj_period:
            # Exclude Adj periods. They are always 0 in the current year
            filter_dict["financial_period_id__lte"] = 12
        # Use annotation to show the name for period 0
        # it does not exist in the financial period model,
        # because it is an artefact for the reports
        archive_period_name_field = "archived_period_name"
        archive_period_code_field = "archived_period_code"
        financial_period_code_field = "financial_period_code"

        annotation_dict = {
            market_field: Coalesce(self.market_field, Value("0")),
            contract_field: Coalesce(self.contract_field, Value("0")),
            project_field: Coalesce(self.project_field, Value("0")),
            archive_period_name_field: Coalesce(
                "archived_period__period_short_name", Value(ARCHIVED_PERIOD_0_NAME)
            ),
            archive_period_name_field: Coalesce(
                "archived_period__period_short_name", Value(ARCHIVED_PERIOD_0_NAME)
            ),
            archive_period_code_field: Coalesce(
                "archived_period__financial_period_code", 0
            ),
            financial_period_code_field: Coalesce(
                "financial_period__financial_period_code", 0
            ),
            "archiving_year": ExpressionWrapper(
                Value(current_year), output_field=IntegerField()
            ),
        }

        forecast_queryset = (
            queryset.objects.select_related(*self.select_related_list)
            .filter(**filter_dict)
            # .filter(
            #     financial_code__cost_centre__cost_centre_code__in=[
            #         "109075",
            #         "109451",
            #         "109714",
            #         "109838",
            #     ]
            # )
            .annotate(**annotation_dict)
            .values_list(
                *self.chart_of_account_field_list,
                "financial_code",
                *self.data_field_list,
                financial_period_code_field,
                "financial_period__period_short_name",
                archive_period_code_field,
                archive_period_name_field,
                "financial_year_id",
                "archiving_year",
            )
        )
        for row in forecast_queryset:
            writer.writerow(row)
