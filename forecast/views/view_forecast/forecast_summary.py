from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import reverse
from django.views.generic.base import TemplateView

from costcentre.forms import DirectorateCostCentresForm
from costcentre.models import (
    CostCentre,
    Directorate,
)
from costcentre.models import DepartmentalGroup

from forecast.forms import ForecastPeriodForm
from forecast.tables import (
    ForecastSubTotalTable,
    ForecastWithLinkTable,
)
from forecast.utils.query_fields import (
    BUDGET_CATEGORY_ID,
    BUDGET_CATEGORY_NAME,
    BUDGET_TYPE,
    FORECAST_EXPENDITURE_TYPE_NAME,
    PROGRAMME_CODE,
    PROGRAMME_NAME,
    PROJECT_CODE,
    PROJECT_NAME,
    SHOW_COSTCENTRE,
    SHOW_DIRECTORATE,
    SHOW_DIT,
    SHOW_GROUP,
    expenditure_columns,
    expenditure_display_sub_total_column,
    expenditure_order_list,
    expenditure_sub_total,
    expenditure_view,
    filter_codes,
    filter_selectors,
    hierarchy_columns,
    hierarchy_order_list,
    hierarchy_sub_total,
    hierarchy_sub_total_column,
    hierarchy_view,
    hierarchy_view_code,
    hierarchy_view_link_column,
    programme_columns,
    programme_detail_view,
    programme_display_sub_total_column,
    programme_order_list,
    programme_sub_total,
    project_columns,
    project_detail_view,
    project_display_sub_total_column,
    project_order_list,
    project_sub_total,
)
from forecast.views.base import (
    ForecastViewPermissionMixin,
    ForecastViewTableMixin,
    PeriodView,
)


class ForecastMultiTableMixin(ForecastViewTableMixin):
    hierarchy_type = -1

    def class_name(self):
        return "wide-table"

    def get_tables(self):
        """
         Return an array of table instances containing data.
        """
        filter_code = ""
        pivot_filter = {}
        arg_name = filter_codes[self.hierarchy_type]
        if arg_name:
            filter_code = self.kwargs[arg_name]
            pivot_filter = {filter_selectors[self.hierarchy_type]: f"{filter_code}"}

        hierarchy_data = self.data_model.view_data.subtotal_data(
            hierarchy_sub_total_column[self.hierarchy_type],
            hierarchy_sub_total,
            hierarchy_columns[self.hierarchy_type].keys(),
            pivot_filter,
            order_list=hierarchy_order_list,
        )
        programme_data = self.data_model.view_data.subtotal_data(
            programme_display_sub_total_column,
            programme_sub_total,
            programme_columns.keys(),
            pivot_filter,
            order_list=programme_order_list,
        )

        expenditure_data = self.data_model.view_data.subtotal_data(
            expenditure_display_sub_total_column,
            expenditure_sub_total,
            expenditure_columns.keys(),
            pivot_filter,
            order_list=expenditure_order_list,
        )

        # In the project report, exclude rows without a project code.
        k = f"{PROJECT_CODE}__isnull"
        pivot_filter.update({k: False})
        project_data = self.data_model.view_data.subtotal_data(
            project_display_sub_total_column,
            project_sub_total,
            project_columns.keys(),
            pivot_filter,
            order_list=project_order_list,
        )

        if self.hierarchy_type == SHOW_COSTCENTRE:
            programme_table = ForecastSubTotalTable(
                programme_columns, programme_data, actual_month_list=self.month_list,
            )
        else:
            programme_table = ForecastWithLinkTable(
                PROGRAMME_NAME,
                programme_detail_view[self.hierarchy_type],
                [PROGRAMME_CODE, FORECAST_EXPENDITURE_TYPE_NAME, self.period],
                filter_code,
                programme_columns,
                programme_data,
                actual_month_list=self.month_list,
            )

        programme_table.attrs["caption"] = "Control total report"
        programme_table.tag = self.table_tag

        expenditure_table = ForecastWithLinkTable(
            BUDGET_CATEGORY_NAME,
            expenditure_view[self.hierarchy_type],
            [BUDGET_CATEGORY_ID, BUDGET_TYPE, self.period],
            filter_code,
            expenditure_columns,
            expenditure_data,
            actual_month_list=self.month_list,
        )
        expenditure_table.attrs["caption"] = "Expenditure report"
        expenditure_table.tag = self.table_tag

        project_table = ForecastWithLinkTable(
            PROJECT_NAME,
            project_detail_view[self.hierarchy_type],
            [PROJECT_CODE, self.period],
            filter_code,
            project_columns,
            project_data,
            actual_month_list=self.month_list,
        )
        project_table.attrs["caption"] = "Project report"
        project_table.tag = self.table_tag

        if self.hierarchy_type == SHOW_COSTCENTRE:
            hierarchy_table = ForecastSubTotalTable(
                hierarchy_columns[self.hierarchy_type],
                hierarchy_data,
                actual_month_list=self.month_list,
            )
        else:
            hierarchy_table = ForecastWithLinkTable(
                hierarchy_view_link_column[self.hierarchy_type],
                hierarchy_view[self.hierarchy_type],
                [hierarchy_view_code[self.hierarchy_type], self.period],
                "",
                hierarchy_columns[self.hierarchy_type],
                hierarchy_data,
                actual_month_list=self.month_list,
            )

        hierarchy_table.attrs["caption"] = "Forecast hierarchy report"
        hierarchy_table.tag = self.table_tag

        self.tables = [
            hierarchy_table,
            programme_table,
            expenditure_table,
            project_table,
        ]

        return self.tables


class DITView(ForecastViewPermissionMixin, ForecastMultiTableMixin, PeriodView):
    template_name = "forecast/view/dit.html"
    table_pagination = False
    hierarchy_type = SHOW_DIT

    def post(self, request, *args, **kwargs):
        new_period = request.POST.get("selected_period", None,)
        return HttpResponseRedirect(
            reverse("forecast_dit", kwargs={"period": new_period})
        )


class GroupView(
    ForecastViewPermissionMixin, ForecastMultiTableMixin, PeriodView,
):
    template_name = "forecast/view/group.html"
    table_pagination = False
    hierarchy_type = SHOW_GROUP

    def group(self):
        return DepartmentalGroup.objects.get(
            group_code=self.kwargs["group_code"], active=True,
        )

    def post(self, request, *args, **kwargs):
        new_period = request.POST.get("selected_period", None,)
        return HttpResponseRedirect(
            reverse(
                "forecast_group",
                kwargs={
                    "group_code": self.kwargs["group_code"],
                    "period": new_period,
                },
            )
        )


class DirectorateView(
    ForecastViewPermissionMixin, ForecastMultiTableMixin, PeriodView,
):
    template_name = "forecast/view/directorate.html"
    table_pagination = False
    hierarchy_type = SHOW_DIRECTORATE

    def directorate(self):
        return Directorate.objects.get(
            directorate_code=self.kwargs["directorate_code"], active=True,
        )

    def post(self, request, *args, **kwargs):
        new_period = request.POST.get("selected_period", None,)
        return HttpResponseRedirect(
            reverse(
                "forecast_directorate",
                kwargs={
                    "directorate_code": self.kwargs["directorate_code"],
                    "period": new_period,
                },
            )
        )


class CostCentreView(
    ForecastViewPermissionMixin, ForecastMultiTableMixin, TemplateView
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
            cost_centre_code=cost_centre.cost_centre_code,
            directorate_code=cost_centre.directorate.directorate_code,
        )

    def period_form(self):
        return ForecastPeriodForm(selected_period=self.period)

    def post(self, request, *args, **kwargs):
        selected_period = request.POST.get("selected_period", None,)
        if selected_period is None:
            cost_centre_code = request.POST.get("cost_centre", None,)
            if cost_centre_code:
                return HttpResponseRedirect(
                    reverse(
                        "forecast_cost_centre",
                        kwargs={
                            "cost_centre_code": cost_centre_code,
                            "period": self.period,
                        },
                    )
                )
            else:
                raise Http404("Cost Centre not found")
        else:
            if selected_period != self.period:
                return HttpResponseRedirect(
                    reverse(
                        "forecast_cost_centre",
                        kwargs={
                            "cost_centre_code": self.cost_centre().cost_centre_code,
                            "period": selected_period,
                        },
                    )
                )
