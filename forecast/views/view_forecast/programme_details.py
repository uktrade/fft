from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import reverse

from chartofaccountDIT.forms import ProgrammeForm

from forecast.tables import ForecastSubTotalTable
from forecast.views.base import (
    DITForecastMixin,
    DirectorateForecastMixin,
    ForecastViewPermissionMixin,
    ForecastViewTableMixin,
    GroupForecastMixin,
)


class ForecastProgrammeDetailsMixin(ForecastViewTableMixin):

    def class_name(self):
        return "wide-table"

    def programme_code(self):
        return self.field_infos.programme_code(self.kwargs["programme_code"])

    def forecast_expenditure_type(self):
        return self.kwargs["forecast_expenditure_type"]

    def programme_code_form(self):
        return ProgrammeForm(
            programme_code=self.kwargs["programme_code"],
            year=self.year
        )

    def post(self, request, *args, **kwargs):
        self.selected_period = request.POST.get("selected_period", None,)
        if self.selected_period is None:
            self.selected_period = self.period
            # Check that a programme code was selected
            self.selected_programme_code_id = request.POST.get("programme_code", None,)
            if self.selected_programme_code_id is None:
                raise Http404("Programme code not found")
        else:
            self.selected_programme_code_id = self.kwargs["programme_code"]
        return HttpResponseRedirect(
            reverse(self.url_name, kwargs=self.selection_kwargs(),)
        )

    def get_tables(self):
        """
         Return an array of table instances containing data.
        """
        forecast_expenditure_type_name = self.kwargs["forecast_expenditure_type"]
        programme_code_id = self.kwargs["programme_code"]
        self.field_infos.hierarchy_type = self.hierarchy_type
        pivot_filter = {
            self.field_infos.programme_code_field: f"{programme_code_id}",
            self.field_infos.expenditure_type_name_field: f"{forecast_expenditure_type_name}",  # noqa
        }
        arg_name = self.field_infos.filter_codes
        if arg_name:
            filter_code = self.kwargs[arg_name]
            pivot_filter[self.field_infos.filter_selector] = f"{filter_code}"

        columns = self.field_infos.programme_details_hierarchy_columns
        programme_details_data = self.data_model.view_data.subtotal_data(
            self.field_infos.programme_details_display_sub_total_column,
            self.field_infos.programme_details_sub_total,
            columns.keys(),
            pivot_filter,
            order_list=self.field_infos.programme_details_hierarchy_order_list,
            show_grand_total=False,
        )

        programme_details_table = ForecastSubTotalTable(
            columns,
            programme_details_data,
            actual_month_list=self.month_list,
            adj_visible_list=self.adj_visible_list,
        )
        programme_details_table.attrs["caption"] = "Programme Report"
        programme_details_table.tag = self.table_tag

        self.tables = [
            programme_details_table,
        ]
        return self.tables


class DITProgrammeDetailsView(
    ForecastViewPermissionMixin, ForecastProgrammeDetailsMixin, DITForecastMixin,
):
    template_name = "forecast/view/programme_details/dit.html"
    url_name = "programme_details_dit"

    def class_name(self):
        return "wide-table"

    def selection_kwargs(self):
        return {
            "programme_code": self.selected_programme_code_id,
            "forecast_expenditure_type": self.forecast_expenditure_type(),
            "period": self.selected_period,
        }


class GroupProgrammeDetailsView(
    ForecastViewPermissionMixin, ForecastProgrammeDetailsMixin, GroupForecastMixin,
):
    template_name = "forecast/view/programme_details/group.html"
    url_name = "programme_details_group"

    def selection_kwargs(self):
        return {
            "group_code": self.kwargs["group_code"],
            "programme_code": self.selected_programme_code_id,
            "forecast_expenditure_type": self.forecast_expenditure_type(),
            "period": self.selected_period,
        }


class DirectorateProgrammeDetailsView(
    ForecastViewPermissionMixin,
    ForecastProgrammeDetailsMixin,
    DirectorateForecastMixin,
):
    template_name = "forecast/view/programme_details/directorate.html"
    url_name = "programme_details_directorate"

    def selection_kwargs(self):
        return {
            "directorate_code": self.kwargs["directorate_code"],
            "programme_code": self.selected_programme_code_id,
            "forecast_expenditure_type": self.forecast_expenditure_type(),
            "period": self.selected_period,
        }
