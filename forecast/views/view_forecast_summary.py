from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import (
    reverse,
)
from django.views.generic.base import TemplateView

from django_tables2 import (
    MultiTableMixin,
)

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
)
from forecast.views.base import ForecastViewPermissionMixin
from forecast.views.view_forecast_queries import (
    SHOW_COSTCENTRE,
    SHOW_DIRECTORATE,
    SHOW_DIT,
    SHOW_GROUP,
    display_sub_total_column_nac,
    display_sub_total_column_prog,
    filter_codes, filter_selectors,
    hierarchy_query,
    hierarchy_sub_total_column,
    natural_account_columns,
    order_list_hierarchy,
    order_list_nac,
    order_list_prog,
    programme_columns,
    sub_total_hierarchy,
    sub_total_nac,
    sub_total_prog
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
            group_code=self.kwargs[filter_codes[self.hierarchy_type]],
            active=True,
        )

    def directorates(self):
        return Directorate.objects.filter(
            group__group_code=self.kwargs[filter_codes[self.hierarchy_type]],
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
            directorate_code=self.kwargs[filter_codes[self.hierarchy_type]],
            active=True,
        )

    def cost_centres_form(self):
        return DirectorateCostCentresForm(
            directorate_code=self.kwargs[filter_codes[self.hierarchy_type]]
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
            cost_centre_code=self.kwargs[filter_codes[self.hierarchy_type]],
        )

    def cost_centres_form(self):
        cost_centre = self.cost_centre()

        return DirectorateCostCentresForm(
            directorate_code=cost_centre.directorate.directorate_code
        )

    def post(self, request, *args, **kwargs):
        cost_centre_code = request.POST.get(
            filter_codes[self.hierarchy_type],
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
