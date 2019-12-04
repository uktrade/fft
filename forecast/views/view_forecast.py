from django.views.generic.base import TemplateView

from django_tables2 import (
    MultiTableMixin,
)

from forecast.models import (
    MonthlyFigure,
)
from forecast.tables import (
    ForecastSubTotalTable,
)
from forecast.views.base import ForecastViewPermissionMixin
from forecast.views.view_forecast_queries import (
    cost_centre_columns,
    expenditure_columns,
    programme_columns,
)

TEST_COST_CENTRE = 109076
TEST_FINANCIAL_YEAR = 2019


def get_forecast_table():
    # TODO remove hardcoded cost centre
    # TODO the filter will be set from the request

    cost_centre_code = TEST_COST_CENTRE
    order_list = ["programme__budget_type_fk__budget_type_display_order"]
    pivot_filter = {"cost_centre__cost_centre_code": "{}".format(cost_centre_code)}

    sub_total_type = ["programme__budget_type_fk__budget_type_display"]
    display_sub_total_column = "cost_centre__cost_centre_name"
    q1 = MonthlyFigure.pivot.subtotal_data(
        display_sub_total_column,
        sub_total_type,
        cost_centre_columns.keys(),
        pivot_filter,
        order_list=order_list,
    )

    # subtotal_data
    order_list_prog = [
        "programme__budget_type_fk__budget_type_display_order",
        "forecast_expenditure_type__forecast_expenditure_type_display_order",
    ]
    sub_total_prog = [
        "programme__budget_type_fk__budget_type_display",
        "forecast_expenditure_type__forecast_expenditure_type_description",
    ]
    display_sub_total_column = "programme__programme_description"

    q2 = MonthlyFigure.pivot.subtotal_data(
        display_sub_total_column,
        sub_total_prog,
        programme_columns.keys(),
        pivot_filter,
        order_list=order_list_prog,
    )

    sub_total_nac = [
        "programme__budget_type_fk__budget_type_display",
        "natural_account_code__expenditure_category__NAC_category__NAC_category_description",  # noqa
    ]
    display_sub_total_column = (
        "natural_account_code__expenditure_category__grouping_description"
    )
    order_list_nac = [
        "programme__budget_type_fk__budget_type_display_order",
        "natural_account_code__expenditure_category__NAC_category__NAC_category_description", # noqa
    ]

    q3 = MonthlyFigure.pivot.subtotal_data(
        display_sub_total_column,
        sub_total_nac,
        expenditure_columns.keys(),
        pivot_filter,
        order_list=order_list_nac,
    )
    return [
        ForecastSubTotalTable(cost_centre_columns, q1),
        ForecastSubTotalTable(programme_columns, q2),
        ForecastSubTotalTable(expenditure_columns, q3),
    ]


class MultiForecastView(
    ForecastViewPermissionMixin,
    MultiTableMixin,
    TemplateView,
):
    template_name = "forecast/forecastmulti.html"

    table_pagination = False

    def __init__(self, *args, **kwargs):
        self.tables = get_forecast_table()
        super().__init__(*args, **kwargs)
