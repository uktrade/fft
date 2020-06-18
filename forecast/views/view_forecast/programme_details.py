from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import reverse

from chartofaccountDIT.forms import ProgrammeForm
from chartofaccountDIT.models import ProgrammeCode

from costcentre.models import (
    DepartmentalGroup,
    Directorate,
)

from forecast.tables import ForecastSubTotalTable
from forecast.utils.query_fields import (
    FORECAST_EXPENDITURE_TYPE_NAME,
    PROGRAMME_CODE,
    SHOW_DIRECTORATE,
    SHOW_DIT,
    SHOW_GROUP,
    filter_codes,
    filter_selectors,
    programme_details_display_sub_total_column,
    programme_details_hierarchy_columns,
    programme_details_hierarchy_order_list,
    programme_details_sub_total,
)
from forecast.views.base import (
    ForecastViewPermissionMixin,
    ForecastViewTableMixin,
    PeriodView,
)


class ForecastProgrammeDetailsMixin(ForecastViewTableMixin):
    hierarchy_type = -1
    table_pagination = False

    def class_name(self):
        return "wide-table"

    def programme_code(self):
        return ProgrammeCode.objects.get(pk=self.kwargs["programme_code"],)

    def forecast_expenditure_type(self):
        return self.kwargs["forecast_expenditure_type"]

    def programme_code_form(self):
        return ProgrammeForm(programme_code=self.kwargs["programme_code"])

    def post(self, request, *args, **kwargs):
        self.selected_period = request.POST.get("selected_period", None,)
        if self.selected_period is None:
            self.selected_period = self.period
            # Check that an expenditure category was selected
            self.selected_programme_code_id = request.POST.get("programme_code", None,)
            if self.selected_programme_code_id is None:
                raise Http404("Budget Type not found")
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
        pivot_filter = {
            PROGRAMME_CODE: f"{programme_code_id}",
            FORECAST_EXPENDITURE_TYPE_NAME: f"{forecast_expenditure_type_name}",
        }
        arg_name = filter_codes[self.hierarchy_type]
        if arg_name:
            filter_code = self.kwargs[arg_name]
            pivot_filter[filter_selectors[self.hierarchy_type]] = f"{filter_code}"

        columns = programme_details_hierarchy_columns[self.hierarchy_type]
        programme_details_data = self.data_model.view_data.subtotal_data(
            programme_details_display_sub_total_column,
            programme_details_sub_total,
            columns.keys(),
            pivot_filter,
            order_list=programme_details_hierarchy_order_list[self.hierarchy_type],
            show_grand_total=False,
        )

        programme_details_table = ForecastSubTotalTable(
            columns, programme_details_data, actual_month_list=self.month_list,
        )
        programme_details_table.attrs["caption"] = "Programme Report"
        programme_details_table.tag = self.table_tag

        self.tables = [
            programme_details_table,
        ]
        return self.tables


class DITProgrammeDetailsView(
    ForecastViewPermissionMixin, ForecastProgrammeDetailsMixin, PeriodView,
):
    template_name = "forecast/view/programme_details/dit.html"
    hierarchy_type = SHOW_DIT
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
    ForecastViewPermissionMixin, ForecastProgrammeDetailsMixin, PeriodView,
):
    template_name = "forecast/view/programme_details/group.html"
    hierarchy_type = SHOW_GROUP
    url_name = "programme_details_group"

    def group(self):
        return DepartmentalGroup.objects.get(
            group_code=self.kwargs["group_code"], active=True,
        )

    def selection_kwargs(self):
        return {
            "group_code": self.group().group_code,
            "programme_code": self.selected_programme_code_id,
            "forecast_expenditure_type": self.forecast_expenditure_type(),
            "period": self.selected_period,
        }


class DirectorateProgrammeDetailsView(
    ForecastViewPermissionMixin, ForecastProgrammeDetailsMixin, PeriodView,
):
    template_name = "forecast/view/programme_details/directorate.html"
    hierarchy_type = SHOW_DIRECTORATE
    url_name = "programme_details_directorate"

    def directorate(self):
        return Directorate.objects.get(
            directorate_code=self.kwargs["directorate_code"], active=True,
        )

    def selection_kwargs(self):
        return {
            "directorate_code": self.kwargs["directorate_code"],
            "programme_code": self.selected_programme_code_id,
            "forecast_expenditure_type": self.forecast_expenditure_type(),
            "period": self.selected_period,
        }
