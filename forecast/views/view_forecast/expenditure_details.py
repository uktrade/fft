from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import (
    reverse,
)
from django.views.generic.base import TemplateView

from django_tables2 import (
    MultiTableMixin,
)

from chartofaccountDIT.models import ExpenditureCategory

from costcentre.forms import (
    ExpenditureTypeForm,
)
from costcentre.models import (
    CostCentre,
    Directorate,
)
from costcentre.models import DepartmentalGroup

from forecast.models import (
    MonthlyFigureAmount,
)
from forecast.tables import (
    ForecastSubTotalTable,
)
from forecast.utils.query_fields import (
    BUDGET_TYPE,
    EXPENDITURE_TYPE_ID,
    SHOW_COSTCENTRE,
    SHOW_DIRECTORATE,
    SHOW_DIT,
    SHOW_GROUP,
    filter_codes,
    filter_selectors,
    nac_columns,
    nac_display_sub_total_column,
    nac_order_list,
    nac_sub_total,
)
from forecast.views.base import ForecastViewPermissionMixin


class ForecastExpenditureDetailsMixin(MultiTableMixin):
    hierarchy_type = -1
    table_pagination = False

    def expenditure_category(self):
        return ExpenditureCategory.objects.get(
            pk=self.kwargs['expenditure_category'],
        )

    def budget_type(self):
        return self.kwargs['budget_type']

    def expenditure_type_form(self):
        return ExpenditureTypeForm()

    def get_tables(self):
        """
         Return an array of table instances containing data.
        """
        budget_type_id = self.kwargs['budget_type']
        expenditure_category_id = self.kwargs['expenditure_category']
        pivot_filter = {
            EXPENDITURE_TYPE_ID: f"{expenditure_category_id}",
            BUDGET_TYPE: f"{budget_type_id}",
        }
        arg_name = filter_codes[self.hierarchy_type]
        if arg_name:
            filter_code = self.kwargs[arg_name]
            pivot_filter[filter_selectors[self.hierarchy_type]] = f"{filter_code}"

        nac_data = MonthlyFigureAmount.pivot.subtotal_data(
            nac_display_sub_total_column,
            nac_sub_total,
            nac_columns.keys(),
            pivot_filter,
            order_list=nac_order_list,
            show_grand_total=False
        )

        nac_table = ForecastSubTotalTable(nac_columns, nac_data)
        nac_table.attrs['caption'] = "Expenditure Report"

        self.tables = [
            nac_table,
        ]
        return self.tables


class DITExpenditureDetailsView(
    ForecastViewPermissionMixin,
    ForecastExpenditureDetailsMixin,
    TemplateView,
):
    template_name = "forecast/view/expenditure_details/dit.html"
    hierarchy_type = SHOW_DIT

    def post(self, request, *args, **kwargs):
        expenditure_category_id = request.POST.get(
            'expenditure_category',
            None,
        )

        if expenditure_category_id:
            return HttpResponseRedirect(
                reverse(
                    "expenditure_details_dit",
                    kwargs={'expenditure_category': expenditure_category_id,
                            'budget_type': self.budget_type(),
                            }

                )
            )
        else:
            raise Http404("Budget Type not found")


class GroupExpenditureDetailsView(
    ForecastViewPermissionMixin,
    ForecastExpenditureDetailsMixin,
    TemplateView,
):
    template_name = "forecast/view/expenditure_details/group.html"
    hierarchy_type = SHOW_GROUP

    def group(self):
        return DepartmentalGroup.objects.get(
            group_code=self.kwargs['group_code'],
            active=True,
        )

    def post(self, request, *args, **kwargs):
        expenditure_category_id = request.POST.get(
            'expenditure_category',
            None,
        )

        if expenditure_category_id:
            return HttpResponseRedirect(
                reverse(
                    "expenditure_details_group",
                    kwargs={'group_code': self.group().group_code,
                            'expenditure_category': expenditure_category_id,
                            'budget_type': self.budget_type(),
                            }
                )
            )
        else:
            raise Http404("Budget Type not found")


class DirectorateExpenditureDetailsView(
    ForecastViewPermissionMixin,
    ForecastExpenditureDetailsMixin,
    TemplateView,
):
    template_name = "forecast/view/expenditure_details/directorate.html"
    hierarchy_type = SHOW_DIRECTORATE

    def directorate(self):
        return Directorate.objects.get(
            directorate_code=self.kwargs['directorate_code'],
            active=True,
        )

    def post(self, request, *args, **kwargs):
        expenditure_category_id = request.POST.get(
            'expenditure_category',
            None,
        )

        if expenditure_category_id:
            return HttpResponseRedirect(
                reverse(
                    "expenditure_details_directorate",
                    kwargs={'directorate_code': self.directorate().directorate_code,
                            'expenditure_category': expenditure_category_id,
                            'budget_type': self.budget_type(),
                            }
                )
            )
        else:
            raise Http404("Budget Type not found")


class CostCentreExpenditureDetailsView(
    ForecastViewPermissionMixin,
    ForecastExpenditureDetailsMixin,
    TemplateView,
):
    template_name = "forecast/view/expenditure_details/cost_centre.html"
    table_pagination = False
    hierarchy_type = SHOW_COSTCENTRE

    def cost_centre(self):
        return CostCentre.objects.get(
            cost_centre_code=self.kwargs['cost_centre_code'],
        )

    def post(self, request, *args, **kwargs):
        expenditure_category_id = request.POST.get(
            'expenditure_category',
            None,
        )

        if expenditure_category_id:
            return HttpResponseRedirect(
                reverse(
                    "expenditure_details_cost_centre",
                    kwargs={'cost_centre_code': self.cost_centre().cost_centre_code,
                            'expenditure_category': expenditure_category_id,
                            'budget_type': self.budget_type(),
                            }
                )
            )
        else:
            raise Http404("Budget Type not found")
