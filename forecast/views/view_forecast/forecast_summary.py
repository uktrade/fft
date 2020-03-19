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
    ForecastingDataView,
)
from forecast.tables import (
    ForecastSubTotalTable,
    ForecastWithLinkTable,
)
from forecast.utils.query_fields import (
    BUDGET_CATEGORY_ID,
    BUDGET_TYPE,
    FORECAST_EXPENDITURE_TYPE_NAME,
    PROGRAMME_CODE,
    PROJECT_CODE,
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
from forecast.views.base import ForecastViewPermissionMixin


class ForecastMultiTableMixin(MultiTableMixin):
    hierarchy_type = -1

    def class_name(self):
        return "wide-table"

    def get_tables(self):
        """
         Return an array of table instances containing data.
        """
        filter_code = ''
        pivot_filter = {}
        arg_name = filter_codes[self.hierarchy_type]
        if arg_name:
            filter_code = self.kwargs[arg_name]
            pivot_filter = {filter_selectors[self.hierarchy_type]: f"{filter_code}"}

        hierarchy_data = ForecastingDataView.view_data.subtotal_data(
            hierarchy_sub_total_column[self.hierarchy_type],
            hierarchy_sub_total,
            hierarchy_columns[self.hierarchy_type].keys(),
            pivot_filter,
            order_list=hierarchy_order_list,
        )
        programme_data = ForecastingDataView.view_data.subtotal_data(
            programme_display_sub_total_column,
            programme_sub_total,
            programme_columns.keys(),
            pivot_filter,
            order_list=programme_order_list,
        )

        expenditure_data = ForecastingDataView.view_data.subtotal_data(
            expenditure_display_sub_total_column,
            expenditure_sub_total,
            expenditure_columns.keys(),
            pivot_filter,
            order_list=expenditure_order_list,
        )

        project_data = ForecastingDataView.view_data.subtotal_data(
            project_display_sub_total_column,
            project_sub_total,
            project_columns.keys(),
            pivot_filter,
            order_list=project_order_list,
        )
        if self.hierarchy_type == SHOW_COSTCENTRE:
            programme_table = ForecastSubTotalTable(programme_columns, programme_data)
        else:
            programme_table = ForecastWithLinkTable(
                programme_detail_view[self.hierarchy_type],
                [PROGRAMME_CODE, FORECAST_EXPENDITURE_TYPE_NAME],
                filter_code,
                programme_columns,
                programme_data
            )

        programme_table.attrs['caption'] = "Control total report"
        expenditure_table = ForecastWithLinkTable(expenditure_view[self.hierarchy_type],
                                                  [BUDGET_CATEGORY_ID, BUDGET_TYPE],
                                                  filter_code,
                                                  expenditure_columns,
                                                  expenditure_data)
        expenditure_table.attrs['caption'] = "Expenditure report"
        # use   # noqa to avoid random flake8 errors for underindent/overindent
        project_table = ForecastWithLinkTable(project_detail_view[self.hierarchy_type],
                                                  [PROJECT_CODE],
                                                  filter_code,
                                                  project_columns,
                                                  project_data)  # noqa
        project_table.attrs['caption'] = "Project report"

        if self.hierarchy_type == SHOW_COSTCENTRE:
            hierarchy_table = ForecastSubTotalTable(
                hierarchy_columns[self.hierarchy_type],
                hierarchy_data
            )
        else:
            hierarchy_table = ForecastWithLinkTable(
                hierarchy_view[self.hierarchy_type],
                hierarchy_view_code[self.hierarchy_type],
                '',
                hierarchy_columns[self.hierarchy_type],
                hierarchy_data)

        self.tables = [
            hierarchy_table,
            programme_table,
            expenditure_table,
            project_table,
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
