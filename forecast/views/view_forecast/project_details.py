from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import reverse

from chartofaccountDIT.forms import ProjectForm

from forecast.tables import ForecastSubTotalTable
from forecast.views.base import (
    CostCentreForecastMixin,
    DITForecastMixin,
    DirectorateForecastMixin,
    ForecastViewPermissionMixin,
    ForecastViewTableMixin,
    GroupForecastMixin,
)


class ForecastProjectDetailsMixin(ForecastViewTableMixin):

    def class_name(self):
        return "wide-table"

    def project_code(self):
        return self.field_infos.project_code(self.kwargs["project_code"])

    def project_code_form(self):
        return ProjectForm(project_code=self.kwargs["project_code"])

    def post(self, request, *args, **kwargs):
        self.selected_period = request.POST.get("selected_period", None,)
        if self.selected_period is None:
            self.selected_period = self.period
            # Check that an expenditure category was selected
            self.selected_project_code_id = request.POST.get("project_code", None,)
            if self.selected_project_code_id is None:
                raise Http404("Project not found")
        else:
            self.selected_project_code_id = self.kwargs["project_code"]
        return HttpResponseRedirect(
            reverse(self.url_name, kwargs=self.selection_kwargs(),)
        )

    def get_tables(self):
        """
         Return an array of table instances containing data.
        """
        self.field_infos.hierarchy_type = self.hierarchy_type
        project_code_id = self.kwargs["project_code"]
        pivot_filter = {
            self.field_infos.project_code_field: f"{project_code_id}",
        }
        arg_name = self.field_infos.filter_codes
        if arg_name:
            filter_code = self.kwargs[arg_name]
            # add the correct hierarchy filter to the pivot
            pivot_filter[self.field_infos.filter_selector] = f"{filter_code}"

        columns = self.field_infos.project_details_hierarchy_columns
        project_details_data = self.data_model.view_data.subtotal_data(
            self.field_infos.project_details_hierarchy_sub_total_column,
            self.field_infos.project_details_sub_total,
            columns.keys(),
            pivot_filter,
            order_list=self.field_infos.project_details_hierarchy_order_list,
            show_grand_total=False,
        )

        project_details_table = ForecastSubTotalTable(
            columns, project_details_data, actual_month_list=self.month_list,
        )
        project_details_table.attrs["caption"] = "Project Report"
        project_details_table.tag = self.table_tag

        self.tables = [
            project_details_table,
        ]

        return self.tables


class DITProjectDetailsView(
    ForecastViewPermissionMixin, ForecastProjectDetailsMixin, DITForecastMixin,
):
    template_name = "forecast/view/project_details/dit.html"
    url_name = "project_details_dit"

    def selection_kwargs(self):
        return {
            "project_code": self.selected_project_code_id,
            "period": self.selected_period,
        }


class GroupProjectDetailsView(
    ForecastViewPermissionMixin, ForecastProjectDetailsMixin, GroupForecastMixin,
):
    template_name = "forecast/view/project_details/group.html"
    url_name = "project_details_group"

    def selection_kwargs(self):
        return {
            "group_code": self.kwargs["group_code"],
            "project_code": self.selected_project_code_id,
            "period": self.selected_period,
        }


class DirectorateProjectDetailsView(
    ForecastViewPermissionMixin, ForecastProjectDetailsMixin, DirectorateForecastMixin,
):
    template_name = "forecast/view/project_details/directorate.html"
    url_name = "project_details_directorate"

    def selection_kwargs(self):
        return {
            "directorate_code": self.kwargs["directorate_code"],
            "project_code": self.selected_project_code_id,
            "period": self.selected_period,
        }


class CostCentreProjectDetailsView(
    ForecastViewPermissionMixin, ForecastProjectDetailsMixin, CostCentreForecastMixin,
):
    template_name = "forecast/view/project_details/cost_centre.html"
    url_name = "project_details_costcentre"

    @property
    def cost_centre_code(self):
        return self.kwargs['cost_centre_code']

    def selection_kwargs(self):
        return {
            "cost_centre_code": self.kwargs["cost_centre_code"],
            "project_code": self.selected_project_code_id,
            "period": self.selected_period,
        }
