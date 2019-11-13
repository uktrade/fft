from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import (
    render,
    reverse,
)
from django.views.generic.base import TemplateView

from django_tables2 import (
    MultiTableMixin,
    RequestConfig,
    SingleTableView,
)

from core.views import FidoExportMixin

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
    ForecastTable,
)


TEST_COST_CENTRE = 888812
TEST_FINANCIAL_YEAR = 2019

# programme__budget_type_fk__budget_type_display
# indicates if DEL, AME, ADMIN used in every view
budget_type_columns = {
    "programme__budget_type_fk__budget_type_display": "Budget_type",
    "cost_centre__cost_centre_name": "Cost Centre Description",
    "cost_centre__cost_centre_code": "Cost Centre Code",
}

programme_columns = {
    "programme__budget_type_fk__budget_type_display": "Hidden",
    "forecast_expenditure_type__forecast_expenditure_type_description": "Hidden",
    "forecast_expenditure_type__forecast_expenditure_type_name": "Expenditure Type",
    "programme__programme_description": "Programme Description",
    "programme__programme_code": "Programme Code",
}

natural_account_columns = {
    "programme__budget_type_fk__budget_type_display": "Hidden",
    "natural_account_code__expenditure_category__NAC_category__NAC_category_description": "Budget Grouping",  # noqa
    "natural_account_code__expenditure_category__grouping_description": "Budget Category",  # noqa
}


class PivotClassView(FidoExportMixin, SingleTableView):
    template_name = "forecast/forecast.html"
    sheet_name = "Forecast"
    filterset_class = None
    table_class = ForecastTable

    table_pagination = False

    def get_table_kwargs(self):
        return {"column_dict": self.column_dict}

    def __init__(self, *args, **kwargs):
        # set the queryset at init, because it
        # requires the current year, so it is
        # recall each time. Maybe an overkill,
        # but I don't want to risk to forget
        # to change the year!
        d1 = {
            "cost_centre__directorate__group": "Group",
            "cost_centre__directorate__group__group_name": "Name",
        }
        q = MonthlyFigure.pivot.pivot_data(d1.keys())
        self.queryset = q
        self.column_dict = d1
        super().__init__(*args, **kwargs)


class CostClassView(FidoExportMixin, SingleTableView):
    template_name = "forecast/forecast.html"
    sheet_name = "Forecast"
    filterset_class = None
    table_class = ForecastTable
    table_pagination = False

    def get_table_kwargs(self):
        return {"column_dict": self.column_dict}

    def __init__(self, *args, **kwargs):
        # set the queryset at init, because it
        # requires the current year, so it is
        # recall each time. Maybe an overkill,
        # but I don't want to risk to forget
        # to change the year!
        columns = {
            "cost_centre__cost_centre_code": "Cost Centre Code",
            "cost_centre__cost_centre_name": "Cost Centre Description",
            "natural_account_code__natural_account_code": "Natural Account Code",
            "natural_account_code__natural_account_code_description": "Natural Account Code Description",  # noqa
            "programme__programme_code": "Programme Code",
            "programme__programme_description": "Programme Description",
            "project_code__project_code": "Project Code",
            "project_code__project_description": "Project Description",
            "programme__budget_type_fk__budget_type_display": "Budget Type",
            "natural_account_code__expenditure_category__NAC_category__NAC_category_description": "Budget Grouping",  # noqa
        # noqa
            "natural_account_code__expenditure_category__grouping_description": "Budget Category",  # noqa
            "natural_account_code__account_L5_code__economic_budget_code": "Expenditure Type",  # noqa
        }
        cost_centre_code = TEST_COST_CENTRE
        pivot_filter = {"cost_centre__cost_centre_code": "{}".format(cost_centre_code)}
        q = MonthlyFigure.pivot.pivot_data(columns.keys(), pivot_filter)
        self.queryset = q
        self.column_dict = columns
        super().__init__(*args, **kwargs)


def get_forecast_table():
    # TODO remove hardcoded cost centre
    # TODO the filter will be set from the request

    cost_centre_code = TEST_COST_CENTRE
    order_list = ["programme__budget_type_fk__budget_type_display_order"]
    pivot_filter = {"cost_centre__cost_centre_code": "{}".format(cost_centre_code)}

    sub_total_type = ["programme__budget_type_fk__budget_type_display"]
    display_sub_total_column = "cost_centre__cost_centre_name"
    q1 = MonthlyFigure.pivot.subtotal_data(
        display_sub_total_column,
        sub_total_type,
        budget_type_columns.keys(),
        pivot_filter,
        order_list=order_list,
    )

    # subtotal_data
    order_list_prog = [
        "programme__budget_type_fk__budget_type_display_order",
        "forecast_expenditure_type__forecast_expenditure_type_display_order",
    ]
    sub_total_prog = [
        "programme__budget_type_fk__budget_type_display",
        "forecast_expenditure_type__forecast_expenditure_type_description",
    ]
    display_sub_total_column = "programme__programme_description"

    q2 = MonthlyFigure.pivot.subtotal_data(
        display_sub_total_column,
        sub_total_prog,
        programme_columns.keys(),
        pivot_filter,
        order_list=order_list_prog,
    )

    sub_total_nac = [
        "programme__budget_type_fk__budget_type_display",
        "natural_account_code__expenditure_category__NAC_category__NAC_category_description",  # noqa
    ]
    display_sub_total_column = (
        "natural_account_code__expenditure_category__grouping_description"
    )
    order_list_nac = [
        "programme__budget_type_fk__budget_type_display_order",
        "natural_account_code__expenditure_category__NAC_category__NAC_category_description"  # noqa
    ]

    q3 = MonthlyFigure.pivot.subtotal_data(
        display_sub_total_column,
        sub_total_nac,
        natural_account_columns.keys(),
        pivot_filter,
        order_list=order_list_nac,
    )
    return [
        ForecastSubTotalTable(budget_type_columns, q1),
        ForecastSubTotalTable(programme_columns, q2),
        ForecastSubTotalTable(natural_account_columns, q3),
    ]


class MultiForecastView(MultiTableMixin, TemplateView):
    template_name = "forecast/forecastmulti.html"

    # table_pagination = {
    #     'per_page': 30
    # }
    table_pagination = False

    def __init__(self, *args, **kwargs):
        self.tables = get_forecast_table()
        super().__init__(*args, **kwargs)


def pivot_test1(request):
    field_dict = {
        "cost_centre__directorate": "Directorate",
        "cost_centre__directorate__directorate_name": "Name",
        "natural_account_code": "NAC",
    }

    q1 = MonthlyFigure.pivot.pivot_data(
        field_dict.keys(), {"cost_centre__directorate__group": "1090AA"}
    )
    table = ForecastTable(field_dict, q1)
    RequestConfig(request).configure(table)
    return render(request, "forecast/forecast.html", {"table": table})


class DITView(MultiTableMixin, TemplateView):
    template_name = "forecast/view/dit.html"
    table_pagination = False

    def groups(self):
        return DepartmentalGroup.objects.filter(
            active=True,
        )

    def __init__(self, *args, **kwargs):
        self.tables = get_forecast_table()
        super().__init__(*args, **kwargs)


class GroupView(MultiTableMixin, TemplateView):
    template_name = "forecast/view/group.html"
    table_pagination = False

    def group(self):
        return DepartmentalGroup.objects.get(
            group_code=self.kwargs['group_code'],
            active=True,
        )

    def directorates(self):
        return Directorate.objects.filter(
            group__group_code=self.kwargs['group_code'],
            active=True,
        )

    def __init__(self, *args, **kwargs):
        self.tables = get_forecast_table()
        super().__init__(*args, **kwargs)


class DirectorateView(MultiTableMixin, TemplateView):
    template_name = "forecast/view/directorate.html"
    table_pagination = False

    def directorate(self):
        return Directorate.objects.get(
            directorate_code=self.kwargs['directorate_code'],
            active=True,
        )

    def cost_centres_form(self):
        return DirectorateCostCentresForm(
            directorate_code=self.kwargs['directorate_code']
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

    def __init__(self, *args, **kwargs):
        self.tables = get_forecast_table()
        super().__init__(*args, **kwargs)


class CostCentreView(MultiTableMixin, TemplateView):
    template_name = "forecast/view/cost_centre.html"
    table_pagination = False

    def cost_centre(self):
        return CostCentre.objects.get(
            cost_centre_code=self.kwargs['cost_centre_code'],
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

    def __init__(self, *args, **kwargs):
        self.tables = get_forecast_table()
        super().__init__(*args, **kwargs)
