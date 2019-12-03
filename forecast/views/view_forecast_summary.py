from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import (
    render,
    reverse,
)
from django.views.generic.base import TemplateView

from django_tables2 import (
    MultiTableMixin,
    RequestConfig,
    SingleTableView,
)

from core.views import FidoExportMixin

from costcentre.forms import (
    DirectorateCostCentresForm,
)
from costcentre.models import (
    CostCentre,
    Directorate,
)
from costcentre.models import DepartmentalGroup

from forecast.models import (
    MonthlyFigure,
)
from forecast.tables import (
    ForecastSubTotalTable,
    ForecastTable,
)
from forecast.views.base import ForecastViewPermissionMixin
from forecast.views.view_forecast_queries import (
    budget_type_cost_centre_columns,
    budget_type_cost_directorate_columns,
    budget_type_cost_group_columns,
    programme_columns,
    natural_account_columns,
)

class ForecastTables(MultiTableMixin):
    order_list_hierarchy = ["programme__budget_type_fk__budget_type_display_order"]

    sub_total_type = ["programme__budget_type_fk__budget_type_display"]
    display_sub_total_column_cost_centre = "cost_centre__cost_centre_name"

    # programme data
    order_list_prog = [
        "programme__budget_type_fk__budget_type_display_order",
        "forecast_expenditure_type__forecast_expenditure_type_display_order",
    ]
    sub_total_prog = [
        "programme__budget_type_fk__budget_type_display",
        "forecast_expenditure_type__forecast_expenditure_type_description",
    ]
    display_sub_total_column_prog = "programme__programme_description"

    # NAC data
    sub_total_nac = [
        "programme__budget_type_fk__budget_type_display",
        "natural_account_code__expenditure_category__NAC_category__NAC_category_description", # noqa
    ]
    display_sub_total_column_nac = (
        "natural_account_code__expenditure_category__grouping_description"
    )
    order_list_nac = [
        "programme__budget_type_fk__budget_type_display_order",
        "natural_account_code__expenditure_category__NAC_category__NAC_category_description", # noqa
    ]

    def get_tables(self):
        """
         Return an array of table instances containing data.
        """
        cost_centre_code = self.kwargs['cost_centre_code']
        self.pivot_filter = {"cost_centre__cost_centre_code": f"{cost_centre_code}"}
        hierarchy_data = MonthlyFigure.pivot.subtotal_data(
            self.display_sub_total_column_cost_centre,
            self.sub_total_type,
            budget_type_cost_centre_columns.keys(),
            self.pivot_filter,
            order_list=self.order_list_hierarchy,
        )
        programme_data = MonthlyFigure.pivot.subtotal_data(
            self.display_sub_total_column_prog,
            self.sub_total_prog,
            programme_columns.keys(),
            self.pivot_filter,
            order_list=self.order_list_prog,
        )

        expenditure_data = MonthlyFigure.pivot.subtotal_data(
            self.display_sub_total_column_nac,
            self.sub_total_nac,
            natural_account_columns.keys(),
            self.pivot_filter,
            order_list=self.order_list_nac,
        )
        self.tables = [
            ForecastSubTotalTable(budget_type_cost_centre_columns, hierarchy_data),
            ForecastSubTotalTable(programme_columns, programme_data),
            ForecastSubTotalTable(natural_account_columns, expenditure_data),
        ]
        return self.tables
class CostCentreView(
    ForecastViewPermissionMixin,
    ForecastTables,
    TemplateView,
):
    template_name = "forecast/view/cost_centre.html"
    table_pagination = False

    def cost_centre(self):
        return CostCentre.objects.get(
            cost_centre_code=self.kwargs['cost_centre_code'],
        )

    def cost_centres_form(self):
        cost_centre = self.cost_centre()

        return DirectorateCostCentresForm(
            directorate_code=cost_centre.directorate.directorate_code
        )

    def post(self, request, *args, **kwargs):
        cost_centre_code = request.POST.get(
            'cost_centre',
            None,
        )
        if cost_centre_code:
            return HttpResponseRedirect(
                reverse(
                    "forecast_cost_centre",
                    kwargs={'cost_centre_code': cost_centre_code}
                )
            )
        else:
            raise Http404("Cost Centre not found")
