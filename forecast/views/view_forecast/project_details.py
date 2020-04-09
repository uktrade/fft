from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import (
    reverse,
)
from django.views.generic.base import TemplateView

from django_tables2 import (
    MultiTableMixin,
)

from chartofaccountDIT.forms import (
    ProjectForm,
)
from chartofaccountDIT.models import ProjectCode

from costcentre.models import (
    CostCentre,
    DepartmentalGroup,
    Directorate,
)

from forecast.models import (
    ForecastingDataView,
)
from forecast.tables import (
    ForecastSubTotalTable,
)
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
from forecast.views.base import ForecastViewPermissionMixin


class ForecastProjectDetailsMixin(MultiTableMixin):
    hierarchy_type = -1
    table_pagination = False

    def class_name(self):
        return "wide-table"

    def project_code(self):
        return ProjectCode.objects.get(
            pk=self.kwargs['project_code'],
        )

    def project_code_form(self):
        return ProjectForm()

    def get_tables(self):
        """
         Return an array of table instances containing data.
        """
        project_code_id = self.kwargs['project_code']
        pivot_filter = {
            PROJECT_CODE: f"{project_code_id}",
        }
        arg_name = filter_codes[self.hierarchy_type]
        if arg_name:
            filter_code = self.kwargs[arg_name]
            pivot_filter[filter_selectors[self.hierarchy_type]] = f"{filter_code}"

        columns = project_details_hierarchy_columns[self.hierarchy_type]
        project_details_data = ForecastingDataView.view_data.subtotal_data(
            project_details_hierarchy_sub_total_column[self.hierarchy_type],
            project_details_sub_total,
            columns.keys(),
            pivot_filter,
            order_list=project_details_hierarchy_order_list[self.hierarchy_type],
            show_grand_total=False
        )

        project_details_table = ForecastSubTotalTable(columns, project_details_data)
        project_details_table.attrs['caption'] = "Project Report"

        self.tables = [
            project_details_table,
        ]

        return self.tables


class DITProjectDetailsView(
    ForecastViewPermissionMixin,
    ForecastProjectDetailsMixin,
    TemplateView,
):
    template_name = "forecast/view/project_details/dit.html"
    hierarchy_type = SHOW_DIT

    def class_name(self):
        return "wide-table"

    def post(self, request, *args, **kwargs):
        project_code_id = request.POST.get(
            'project_code',
            None,
        )

        if project_code_id:
            return HttpResponseRedirect(
                reverse(
                    "project_details_dit",
                    kwargs={'project_code': project_code_id,
                            }
                )
            )
        else:
            raise Http404("Project not found")


class GroupProjectDetailsView(
    ForecastViewPermissionMixin,
    ForecastProjectDetailsMixin,
    TemplateView,
):
    template_name = "forecast/view/project_details/group.html"
    hierarchy_type = SHOW_GROUP

    def group(self):
        return DepartmentalGroup.objects.get(
            group_code=self.kwargs['group_code'],
            active=True,
        )

    def post(self, request, *args, **kwargs):
        project_code_id = request.POST.get(
            'project_code',
            None,
        )

        if project_code_id:
            return HttpResponseRedirect(
                reverse(
                    "project_details_group",
                    kwargs={'group_code': self.group().group_code,
                            'project_code': project_code_id,
                            }
                )
            )
        else:
            raise Http404("Project not found")


class DirectorateProjectDetailsView(
    ForecastViewPermissionMixin,
    ForecastProjectDetailsMixin,
    TemplateView,
):
    template_name = "forecast/view/project_details/directorate.html"
    hierarchy_type = SHOW_DIRECTORATE

    def directorate(self):
        return Directorate.objects.get(
            directorate_code=self.kwargs['directorate_code'],
            active=True,
        )

    def post(self, request, *args, **kwargs):
        project_code_id = request.POST.get(
            'project_code',
            None,
        )

        if project_code_id:
            return HttpResponseRedirect(
                reverse(
                    "project_details_directorate",
                    kwargs={'directorate_code': self.directorate().directorate_code,
                            'project_code': project_code_id,
                            }
                )
            )
        else:
            raise Http404("Project not found")


class CostCentreProjectDetailsView(
    ForecastViewPermissionMixin,
    ForecastProjectDetailsMixin,
    TemplateView,
):
    template_name = "forecast/view/project_details/cost_centre.html"
    table_pagination = False
    hierarchy_type = SHOW_COSTCENTRE

    def cost_centre(self):
        return CostCentre.objects.get(
            cost_centre_code=self.kwargs['cost_centre_code'],
        )

    def post(self, request, *args, **kwargs):
        project_code_id = request.POST.get(
            'project_code',
            None,
        )

        if project_code_id:
            return HttpResponseRedirect(
                reverse(
                    "project_details_costcentre",
                    kwargs={'cost_centre_code': self.cost_centre().cost_centre_code,
                            'project_code': project_code_id,
                            }
                )
            )
        else:
            raise Http404("Project not found")
