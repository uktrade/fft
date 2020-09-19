from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import reverse


from costcentre.forms import DirectorateCostCentresForm

from forecast.forms import ForecastPeriodForm
from forecast.tables import (
    ForecastSubTotalTable,
    ForecastWithLinkTable,
)
from forecast.utils.query_fields import (
    SHOW_COSTCENTRE,
)
from forecast.views.base import (
    CostCentreForecastMixin,
    DITForecastMixin,
    DirectorateForecastMixin,
    ForecastViewPermissionMixin,
    ForecastViewTableMixin,
    GroupForecastMixin,
)


class ForecastMultiTableMixin(ForecastViewTableMixin):

    def class_name(self):
        return "wide-table"

    def get_tables(self):
        """
         Return an array of table instances containing data.
        """
        filter_code = ""
        self.field_infos.hierarchy_type = self.hierarchy_type

        pivot_filter = {}
        arg_name = self.field_infos.filter_codes
        if arg_name:
            filter_code = self.kwargs[arg_name]
            pivot_filter = {self.field_infos.filter_selector: f"{filter_code}"}

        hierarchy_order_list = self.field_infos.hierarchy_order_list
        hierarchy_columns = self.field_infos.hierarchy_columns
        hierarchy_data = self.data_model.view_data.subtotal_data(
            self.field_infos.hierarchy_sub_total_column,
            self.field_infos.hierarchy_sub_total,
            hierarchy_columns.keys(),
            pivot_filter,
            order_list=hierarchy_order_list,
        )
        programme_data = self.data_model.view_data.subtotal_data(
            self.field_infos.programme_display_sub_total_column,
            self.field_infos.programme_sub_total,
            self.field_infos.programme_columns.keys(),
            pivot_filter,
            order_list=self.field_infos.programme_order_list,
        )

        expenditure_data = self.data_model.view_data.subtotal_data(
            self.field_infos.expenditure_display_sub_total_column,
            self.field_infos.expenditure_sub_total,
            self.field_infos.expenditure_columns.keys(),
            pivot_filter,
            order_list=self.field_infos.expenditure_order_list,
        )

        # In the project report, exclude rows without a project code.
        k = f"{self.field_infos.project_code_field}__isnull"
        pivot_filter.update({k: False})
        project_data = self.data_model.view_data.subtotal_data(
            self.field_infos.project_display_sub_total_column,
            self.field_infos.project_sub_total,
            self.field_infos.project_columns.keys(),
            pivot_filter,
            order_list=self.field_infos.project_order_list,
        )

        if self.field_infos.hierarchy_type == SHOW_COSTCENTRE:
            programme_table = ForecastSubTotalTable(
                self.field_infos.programme_columns,
                programme_data,
                actual_month_list=self.month_list,
                adj_visible_list=self.adj_visible_list,
            )
        else:
            programme_table = ForecastWithLinkTable(
                self.field_infos.programme_name_field,
                self.field_infos.programme_detail_view,
                [self.field_infos.programme_code_field,
                 self.field_infos.expenditure_type_name_field,
                 self.period],
                filter_code,
                self.field_infos.programme_columns,
                programme_data,
                actual_month_list=self.month_list,
                adj_visible_list=self.adj_visible_list,
            )

        programme_table.attrs["caption"] = "Control total report"
        programme_table.tag = self.table_tag

        expenditure_table = ForecastWithLinkTable(
            self.field_infos.budget_category_name_field,
            self.field_infos.expenditure_view,
            [
                self.field_infos.budget_category_id_field,
                self.field_infos.budget_type_field,
                self.period,
            ],
            filter_code,
            self.field_infos.expenditure_columns,
            expenditure_data,
            actual_month_list=self.month_list,
            adj_visible_list=self.adj_visible_list,
        )
        expenditure_table.attrs["caption"] = "Expenditure report"
        expenditure_table.tag = self.table_tag

        project_table = ForecastWithLinkTable(
            self.field_infos.project_name_field,
            self.field_infos.project_detail_view,
            [self.field_infos.project_code_field, self.period],
            filter_code,
            self.field_infos.project_columns,
            project_data,
            actual_month_list=self.month_list,
            adj_visible_list=self.adj_visible_list,
        )
        project_table.attrs["caption"] = "Project report"
        project_table.tag = self.table_tag

        if self.field_infos.hierarchy_type == SHOW_COSTCENTRE:
            hierarchy_table = ForecastSubTotalTable(
                hierarchy_columns,
                hierarchy_data,
                actual_month_list=self.month_list,
                adj_visible_list=self.adj_visible_list,
            )
        else:
            hierarchy_table = ForecastWithLinkTable(
                self.field_infos.hierarchy_view_link_column,
                self.field_infos.hierarchy_view,
                [self.field_infos.hierarchy_view_code, self.period],
                "",
                hierarchy_columns,
                hierarchy_data,
                actual_month_list=self.month_list,
                adj_visible_list=self.adj_visible_list,
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


class DITView(ForecastViewPermissionMixin, ForecastMultiTableMixin, DITForecastMixin):
    template_name = "forecast/view/dit.html"

    def post(self, request, *args, **kwargs):
        new_period = request.POST.get("selected_period", None,)
        return HttpResponseRedirect(
            reverse("forecast_dit", kwargs={"period": new_period})
        )


class GroupView(
    ForecastViewPermissionMixin, ForecastMultiTableMixin, GroupForecastMixin,
):
    template_name = "forecast/view/group.html"

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
    ForecastViewPermissionMixin, ForecastMultiTableMixin, DirectorateForecastMixin,
):
    template_name = "forecast/view/directorate.html"

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
    ForecastViewPermissionMixin,
    ForecastMultiTableMixin,
    CostCentreForecastMixin
):
    template_name = "forecast/view/cost_centre.html"

    def cost_centres_form(self):
        cost_centre_code = self.cost_centre_code
        return DirectorateCostCentresForm(
            cost_centre_code=cost_centre_code,
            year=self.year
        )

    @property
    def cost_centre_code(self):
        return self.kwargs['cost_centre_code']

    def period_form(self):
        return ForecastPeriodForm(selected_period=self.period)

    def post(self, request, *args, **kwargs):
        # Checking selected_period is needed to find out if we are posting after
        # changing the period or changing the cost centre
        selected_period = request.POST.get("selected_period", None,)
        if selected_period is None:
            # Cost centre changed
            selected_cost_centre_code = request.POST.get("cost_centre", None,)
            if selected_cost_centre_code:
                return HttpResponseRedirect(
                    reverse(
                        "forecast_cost_centre",
                        kwargs={
                            "cost_centre_code": selected_cost_centre_code,
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
                            "cost_centre_code": self.cost_centre_code,
                            "period": selected_period,
                        },
                    )
                )
