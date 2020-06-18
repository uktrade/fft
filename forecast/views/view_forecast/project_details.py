from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import reverse

from chartofaccountDIT.forms import ProjectForm
from chartofaccountDIT.models import ProjectCode

from costcentre.models import (
    CostCentre,
    DepartmentalGroup,
    Directorate,
)

from forecast.tables import ForecastSubTotalTable
from forecast.utils.query_fields import (
    PROJECT_CODE,
    SHOW_COSTCENTRE,
    SHOW_DIRECTORATE,
    SHOW_DIT,
    SHOW_GROUP,
    filter_codes,
    filter_selectors,
    project_details_hierarchy_columns,
    project_details_hierarchy_order_list,
    project_details_hierarchy_sub_total_column,
    project_details_sub_total,
)
from forecast.views.base import (
    ForecastViewPermissionMixin,
    ForecastViewTableMixin,
    PeriodView,
)


class ForecastProjectDetailsMixin(ForecastViewTableMixin):
    hierarchy_type = -1
    table_pagination = False

    def class_name(self):
        return "wide-table"

    def project_code(self):
        return ProjectCode.objects.get(pk=self.kwargs["project_code"],)

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
        project_code_id = self.kwargs["project_code"]
        pivot_filter = {
            PROJECT_CODE: f"{project_code_id}",
        }
        arg_name = filter_codes[self.hierarchy_type]
        if arg_name:
            filter_code = self.kwargs[arg_name]
            pivot_filter[filter_selectors[self.hierarchy_type]] = f"{filter_code}"

        columns = project_details_hierarchy_columns[self.hierarchy_type]
        project_details_data = self.data_model.view_data.subtotal_data(
            project_details_hierarchy_sub_total_column[self.hierarchy_type],
            project_details_sub_total,
            columns.keys(),
            pivot_filter,
            order_list=project_details_hierarchy_order_list[self.hierarchy_type],
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
    ForecastViewPermissionMixin, ForecastProjectDetailsMixin, PeriodView,
):
    template_name = "forecast/view/project_details/dit.html"
    hierarchy_type = SHOW_DIT
    url_name = "project_details_dit"

    def selection_kwargs(self):
        return {
            "project_code": self.selected_project_code_id,
            "period": self.selected_period,
        }


class GroupProjectDetailsView(
    ForecastViewPermissionMixin, ForecastProjectDetailsMixin, PeriodView,
):
    template_name = "forecast/view/project_details/group.html"
    hierarchy_type = SHOW_GROUP
    url_name = "project_details_group"

    def selection_kwargs(self):
        return {
            "group_code": self.group().group_code,
            "project_code": self.selected_project_code_id,
            "period": self.selected_period,
        }

    def group(self):
        return DepartmentalGroup.objects.get(
            group_code=self.kwargs["group_code"], active=True,
        )


class DirectorateProjectDetailsView(
    ForecastViewPermissionMixin, ForecastProjectDetailsMixin, PeriodView,
):
    template_name = "forecast/view/project_details/directorate.html"
    hierarchy_type = SHOW_DIRECTORATE
    url_name = "project_details_directorate"

    def selection_kwargs(self):
        return {
            "directorate_code": self.directorate().directorate_code,
            "project_code": self.selected_project_code_id,
            "period": self.selected_period,
        }

    def directorate(self):
        return Directorate.objects.get(
            directorate_code=self.kwargs["directorate_code"], active=True,
        )


class CostCentreProjectDetailsView(
    ForecastViewPermissionMixin, ForecastProjectDetailsMixin, PeriodView,
):
    template_name = "forecast/view/project_details/cost_centre.html"
    table_pagination = False
    hierarchy_type = SHOW_COSTCENTRE
    url_name = "project_details_costcentre"

    def selection_kwargs(self):
        return {
            "cost_centre_code": self.cost_centre().cost_centre_code,
            "project_code": self.selected_project_code_id,
            "period": self.selected_period,
        }

    def cost_centre(self):
        return CostCentre.objects.get(cost_centre_code=self.kwargs["cost_centre_code"],)
