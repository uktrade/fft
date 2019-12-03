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
    SHOW_DIT,
    SHOW_GROUP,
    SHOW_DIRECTORATE,
    SHOW_COSTCENTRE,
    budget_type_cost_centre_columns,
    budget_type_cost_directorate_columns,
    budget_type_cost_group_columns,
    programme_columns,
    natural_account_columns,
    display_sub_total_column_cost_centre,
    sub_total_hierarchy,
    order_list_hierarchy,
    display_sub_total_column_prog,
    sub_total_prog,
    display_sub_total_column_nac,
    sub_total_nac,
    hierarchy_query,
    filter_codes,
    filter_selectors,
    order_list_prog,
    order_list_nac,
    hierarchy_sub_total_column,
)

class ForecastMultiTableMixin(MultiTableMixin):
    hierarchy_type = -1
    def get_tables(self):
        """
         Return an array of table instances containing data.
        """
        arg_name = filter_codes[self.hierarchy_type]
        if arg_name:
            filter_code = self.kwargs[arg_name]
            pivot_filter = {filter_selectors[self.hierarchy_type]: f"{filter_code}"}
        else:
            pivot_filter = {}
        hierarchy_data = MonthlyFigure.pivot.subtotal_data(
            hierarchy_sub_total_column[self.hierarchy_type],
            sub_total_hierarchy,
            hierarchy_query[self.hierarchy_type].keys(),
            pivot_filter,
            order_list=order_list_hierarchy,
        )
        programme_data = MonthlyFigure.pivot.subtotal_data(
            display_sub_total_column_prog,
            sub_total_prog,
            programme_columns.keys(),
            pivot_filter,
            order_list=order_list_prog,
        )

        expenditure_data = MonthlyFigure.pivot.subtotal_data(
            display_sub_total_column_nac,
            sub_total_nac,
            natural_account_columns.keys(),
            pivot_filter,
            order_list=order_list_nac,
        )
        self.tables = [
            ForecastSubTotalTable(hierarchy_query[self.hierarchy_type], hierarchy_data),
            ForecastSubTotalTable(programme_columns, programme_data),
            ForecastSubTotalTable(natural_account_columns, expenditure_data),
        ]
        return self.tables


class DITView(
    ForecastViewPermissionMixin,
    ForecastMultiTableMixin,
    TemplateView,
):
    template_name = "forecast/view/dit.html"
    table_pagination = False
    hierarchy_type = SHOW_DIT

    def groups(self):
        return DepartmentalGroup.objects.filter(
            active=True,
        )


class GroupView(
    ForecastViewPermissionMixin,
    ForecastMultiTableMixin,
    TemplateView,
):
    template_name = "forecast/view/group.html"
    table_pagination = False
    hierarchy_type = SHOW_GROUP

    def group(self):
        return DepartmentalGroup.objects.get(
            group_code=self.kwargs['group_code'],
            active=True,
        )

    def directorates(self):
        return Directorate.objects.filter(
            group__group_code=self.kwargs['group_code'],
            active=True,
        )



class DirectorateView(
    ForecastViewPermissionMixin,
    ForecastMultiTableMixin,
    TemplateView,
):
    template_name = "forecast/view/directorate.html"
    table_pagination = False
    hierarchy_type = SHOW_DIRECTORATE

    def directorate(self):
        return Directorate.objects.get(
            directorate_code=self.kwargs['directorate_code'],
            active=True,
        )

    def cost_centres_form(self):
        return DirectorateCostCentresForm(
            directorate_code=self.kwargs['directorate_code']
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



class CostCentreView(
    ForecastViewPermissionMixin,
    ForecastMultiTableMixin,
    TemplateView,
):
    template_name = "forecast/view/cost_centre.html"
    table_pagination = False
    hierarchy_type = SHOW_COSTCENTRE
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
