import json
from core.views import FidoExportMixin

from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django_tables2 import MultiTableMixin, SingleTableView
from django_tables2 import RequestConfig

from costcentre.models import CostCentre
from .models import MonthlyFigure, FinancialPeriod
from .tables import ForecastSubTotalTable, ForecastTable
from .forms import EditForm
from forecast.models import MonthlyFigure
from django.core import serializers
import json

from django.core.serializers.json import DjangoJSONEncoder

# programme__budget_type_fk__budget_type_display indicates if DEL, AME, ADMIN used in every view
budget_type_columns = {
    'programme__budget_type_fk__budget_type_display': 'Budget_type',
    'cost_centre__cost_centre_code': 'Cost Centre Code',
    'cost_centre__cost_centre_name': 'Cost Centre Description',
}

programme_columns = {
    'programme__budget_type_fk__budget_type_display': 'Hidden',
    'forecast_expenditure_type__forecast_expenditure_type_description': 'Hidden',
    'forecast_expenditure_type__forecast_expenditure_type_name': 'Expenditure Type',
    'programme__programme_code': 'Programme Code',
    'programme__programme_description': 'Programme Description'
}

natural_account_columns = {
    'programme__budget_type_fk__budget_type_display': 'Hidden',
    'natural_account_code__expenditure_category__NAC_category__NAC_category_description': 'Budget Grouping',
    'natural_account_code__expenditure_category__grouping_description': 'Budget Category',
}


class PivotClassView(FidoExportMixin, SingleTableView):
    template_name = 'forecast/forecast.html'
    sheet_name = 'Forecast'
    filterset_class = None
    table_class = ForecastTable

    table_pagination = False

    def get_table_kwargs(self):
        return {
            'column_dict': self.column_dict
        }

    def __init__(self, *args, **kwargs):
        # set the queryset at init, because it requires the current year, so it is recall each
        # time. Maybe an overkill, but I don't want to risk to forget to change the year!
        d1 = {'cost_centre__directorate__group': 'Group',
              'cost_centre__directorate__group__group_name': 'Name'}
        q = MonthlyFigure.pivot.pivotdata(d1.keys())
        self.queryset = q
        self.column_dict = d1
        super().__init__(*args, **kwargs)


class CostClassView(FidoExportMixin, SingleTableView):
    template_name = 'forecast/forecast.html'
    sheet_name = 'Forecast'
    filterset_class = None
    table_class = ForecastTable
    table_pagination = False

    def get_table_kwargs(self):
        return {
            'column_dict': self.column_dict
        }

    def __init__(self, *args, **kwargs):
        # set the queryset at init, because it requires the current year, so it is recall each
        # time. Maybe an overkill, but I don't want to risk to forget to change the year!
        columns = {'cost_centre__cost_centre_code': 'Cost Centre Code',
                   'cost_centre__cost_centre_name': 'Cost Centre Description',
                   'natural_account_code__natural_account_code': 'Natural Account Code',
                   'natural_account_code__natural_account_code_description': 'Natural Account Code Description',
                   'programme__programme_code': 'Programme Code',
                   'programme__programme_description': 'Programme Description',
                   'project_code__project_code': 'Project Code',
                   'project_code__project_description': 'Project Description',
                   'programme__budget_type_fk__budget_type_display': 'Budget Type',
                   'natural_account_code__expenditure_category__NAC_category__NAC_category_description': 'Budget Grouping',
                   'natural_account_code__expenditure_category__grouping_description': 'Budget Category',
                   'natural_account_code__account_L5_code__economic_budget_code': 'Expenditure Type',
                   }
        cost_centre_code = 888812
        pivot_filter = {'cost_centre__cost_centre_code': '{}'.format(cost_centre_code)}
        q = MonthlyFigure.pivot.pivotdata(columns.keys(), pivot_filter)
        self.queryset = q
        self.column_dict = columns
        super().__init__(*args, **kwargs)


class MultiforecastView(
    MultiTableMixin,
    TemplateView
):
    template_name = 'forecast/forecastmulti.html'

    # table_pagination = {
    #     'per_page': 30
    # }
    table_pagination = False

    def __init__(self, *args, **kwargs):
        # TODO remove hardcoded cost centre
        # TODO the filter will be set from the request
        cost_centre_code = 888812
        order_list = ['programme__budget_type_fk__budget_type_display_order']
        pivot_filter = {'cost_centre__cost_centre_code': '{}'.format(cost_centre_code)}

        sub_total_type = ['programme__budget_type_fk__budget_type_display']
        display_sub_total_column = 'cost_centre__cost_centre_name'
        q1 = MonthlyFigure.pivot.subtotal_data(display_sub_total_column, sub_total_type,
                                               budget_type_columns.keys(),pivot_filter, order_list = order_list)
        # subtotal_data
        order_list = ['programme__budget_type_fk__budget_type_display_order',
                      'forecast_expenditure_type__forecast_expenditure_type_display_order']
        sub_total_prog = ['programme__budget_type_fk__budget_type_display',
                    'forecast_expenditure_type__forecast_expenditure_type_description']
        display_sub_total_column = 'programme__programme_description'
        q2 = MonthlyFigure.pivot.subtotal_data(display_sub_total_column, sub_total_prog, programme_columns.keys(),pivot_filter, order_list = order_list)

        sub_total_nac = ['programme__budget_type_fk__budget_type_display',
                    'natural_account_code__expenditure_category__NAC_category__NAC_category_description']
        display_sub_total_column = 'natural_account_code__expenditure_category__grouping_description'

        q3 = MonthlyFigure.pivot.subtotal_data(display_sub_total_column, sub_total_nac,
                                                natural_account_columns.keys(),pivot_filter, order_list = order_list)
        self.tables = [
            ForecastSubTotalTable(budget_type_columns, q1),
            ForecastSubTotalTable(programme_columns, q2),
            ForecastSubTotalTable(natural_account_columns, q3)
        ]

        super().__init__(*args, **kwargs)


def pivot_test1(request):
    field_dict = {'cost_centre__directorate': 'Directorate',
                  'cost_centre__directorate__directorate_name': 'Name',
                  'natural_account_code': 'NAC'}

    q1 = MonthlyFigure.pivot.pivotdata(field_dict.keys(),
                                       {'cost_centre__directorate__group': '1090AA'})
    table = ForecastTable(field_dict, q1)
    RequestConfig(request).configure(table)
    return render(request, 'forecast/forecast.html', {'table': table})


class EditForecastView(
    UserPassesTestMixin,
    TemplateView,
):
    template_name = "forecast/edit.html"
    cost_centre_code = "888812"

    def test_func(self):
        cost_centre = CostCentre.objects.get(
            cost_centre_code=self.cost_centre_code
        )
        return self.request.user.has_perm('change_cost_centre', cost_centre)

    def handle_no_permission(self):
        return redirect('costcentre')

    def cost_centre_details(self):
        return {
            'group': 'Test group',
            'directorate': 'Test directorate',
            'cost_centre_name': 'Test cost centre name',
            'cost_centre_num': self.cost_centre_code,
        }

    def table(self):
        field_dict = {
            'cost_centre__directorate': 'Directorate',
            'cost_centre__directorate__directorate_name': 'Name',
            'natural_account_code': 'NAC',
            'cost_centre': self.cost_centre_code,
        }

        q1 = MonthlyFigure.pivot.pivotdata(
            field_dict.keys(),
            {'cost_centre': self.cost_centre_code}
        )

        return ForecastTable(field_dict, q1)


def edit_forecast_prototype(request):
    financial_year = 2019
    cost_centre_code = "888812"

    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            cost_centre_code = form.cleaned_data['cost_centre_code']
            financial_year = form.cleaned_data['financial_year']

            cell_data = json.loads(
                form.cleaned_data['cell_data']
            )

            for key, cell in cell_data.items():
                if cell["editable"]:
                    monthly_figure = MonthlyFigure.objects.filter(
                        cost_centre__cost_centre_code=cost_centre_code,
                        financial_year__financial_year=financial_year,
                        financial_period__period_short_name__iexact=cell["key"],
                        programme__programme_code=cell["programmeCode"],
                        natural_account_code__natural_account_code=cell["naturalAccountCode"],
                    ).first()
                    monthly_figure.amount = int(float(cell["value"]))
                    monthly_figure.save()
    else:
        form = EditForm(
            initial={
                'financial_year': financial_year,
                'cost_centre_code': cost_centre_code
            }
        )
    pivot_filter = {'cost_centre__cost_centre_code': '{}'.format(cost_centre_code)}
    monthly_figures = MonthlyFigure.pivot.pivotdata({}, pivot_filter)

    # TODO - Luisella to restrict to financial year
    editable_periods = list(
        FinancialPeriod.objects.filter(
            actual_loaded=False,
        ).all()
    )

    editable_periods_dump = serializers.serialize(
        "json", editable_periods
    )

    forecast_dump = json.dumps(
        list(monthly_figures),
        cls=DjangoJSONEncoder
    )

    return render(
        request,
        'forecast/edit.html',
        {
            'form': form,
            'editable_periods_dump': editable_periods_dump,
            'forecast_dump': forecast_dump,
        }
    )
