import json
from core.views import FidoExportMixin

from django.shortcuts import render
from django.views.generic.base import TemplateView

from django_tables2 import MultiTableMixin, SingleTableView
from django_tables2 import RequestConfig

from .models import MonthlyFigure, FinancialPeriod
from .tables import ForecastSubTotalTable, ForecastTable
from .forms import EditForm
from forecast.models import MonthlyFigure
from django.core import serializers
import json

from django.core.serializers.json import DjangoJSONEncoder

# programme__budget_type_fk__budget_type indicates if DEL, AME, ADMIN used in every view
budget_type_columns = {
    'programme__budget_type_fk__budget_type': 'Budget_type',
    'cost_centre__cost_centre_code': 'Cost Centre Code',
    'cost_centre__cost_centre_name': 'Cost Centre Description',
}

programme_columns = {
    'programme__budget_type_fk__budget_type': 'Hidden',
    'natural_account_code__account_L5_code__economic_budget_code': 'Expenditure Type',
    'programme__programme_code': 'Programme Code',
    'programme__programme_description': 'Programme Description'
}

natural_account_columns = {
    'programme__budget_type_fk__budget_type': 'Hidden',
    'natural_account_code__expenditure_category__NAC_category__NAC_category_description': 'Budget Grouping',
    'natural_account_code__expenditure_category__grouping_description': 'Budget Category',
}


class PivotClassView(FidoExportMixin, SingleTableView):
    template_name = 'forecast/forecast.html'
    sheet_name = 'Forecast'
    filterset_class = None
    table_class = ForecastTable

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
                   'project_code__project_description': 'Programme Description',
                   }
        cost_centre_code = 888812
        pivot_filter = {'cost_centre__cost_centre_code': '{}'.format(cost_centre_code)}
        q = MonthlyFigure.pivot.pivotdata(columns.keys(), pivot_filter)
        self.queryset = q
        self.column_dict = columns
        super().__init__(*args, **kwargs)


class MultiforecastView(MultiTableMixin, TemplateView):
    template_name = 'forecast/forecastmulti.html'

    table_pagination = {
        'per_page': 30
    }

    def __init__(self, *args, **kwargs):
        # TODO remove hardcoded cost centre
        # TODO Add a field to the chart of account tables specifying the row display order
        # TODO the filter will be set from the request
        cost_centre_code = 888812
        order_list = ['-programme__budget_type_fk__budget_type']
        pivot_filter = {'cost_centre__cost_centre_code': '{}'.format(cost_centre_code)}
        # set the queryset at init, because it requires the current year, so it is recall each
        # time. Maybe an overkill, but I don't want to risk to forget to change the year!
        q1 = MonthlyFigure.pivot.pivotdata(budget_type_columns.keys(),pivot_filter, order_list = order_list)
        # subtotal_data
        sub_totals = ['programme__budget_type_fk__budget_type',
                    'natural_account_code__account_L5_code__economic_budget_code']
        display_sub_total_column = 'programme__programme_description'

        # q2 = MonthlyFigure.pivot.pivotdata(programme_columns.keys(),pivot_filter, order_list = order_list)
        q4 = MonthlyFigure.pivot.pivotdata(programme_columns.keys(),pivot_filter, order_list = order_list)
        q2 = MonthlyFigure.pivot.subtotal_data(display_sub_total_column, sub_totals, programme_columns.keys(),pivot_filter, order_list = order_list)
        q3 = MonthlyFigure.pivot.pivotdata(natural_account_columns.keys(),pivot_filter, order_list = order_list)
        self.tables = [
            # ForecastTable(budget_type_columns, q1),
            ForecastSubTotalTable(programme_columns, q2),
            ForecastTable(programme_columns, q4),
            ForecastTable(natural_account_columns, q3)
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


def edit_forecast(request):
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
