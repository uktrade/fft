from core.views import FidoExportMixin

from django.shortcuts import render
from django.views.generic.base import TemplateView

from django_tables2 import MultiTableMixin, SingleTableView
from django_tables2 import RequestConfig

from .models import MonthlyFigure
from .tables import ForecastTable
from .forms import EditForm


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


class MultiforecastView(MultiTableMixin, TemplateView):
    template_name = 'forecast/forecastmulti.html'

    table_pagination = {
        'per_page': 30
    }

    def __init__(self, *args, **kwargs):
        # set the queryset at init, because it requires the current year, so it is recall each
        # time. Maybe an overkill, but I don't want to risk to forget to change the year!
        d1 = {'cost_centre__directorate__group': 'Group',
              'cost_centre__directorate__group__group_name': 'Name'}
        q1 = MonthlyFigure.pivot.pivotdata(d1.keys())
        d2 = {'programme__budget_type_fk__budget_type': 'Programme'}
        q2 = MonthlyFigure.pivot.pivotdata(d2.keys())
        d3 = {'natural_account_code__expenditure_category__NAC_category__NAC_category_description': 'Expenditure Type'}
        q3 = MonthlyFigure.pivot.pivotdata(d3.keys())
        self.tables = [
            ForecastTable(d1, q1),
            ForecastTable(d2, q2),
            ForecastTable(d3, q3)
        ]

        super().__init__(*args, **kwargs)


def pivot_test1(request):
    field_dict = {'cost_centre__directorate': 'Directorate',
                  'cost_centre__directorate__directorate_name': 'Name'}

    q1 = MonthlyFigure.pivot.pivotdata(field_dict.keys(),
                                       {'cost_centre__directorate__group': '1090AA'})
    table = ForecastTable(field_dict, q1)
    RequestConfig(request).configure(table)
    return render(request, 'forecast/forecast.html', {'table': table})


def edit_forecast(request):
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = EditForm()

    return render(
        request,
        'forecast/edit.html',
        {'form': form}
    )
