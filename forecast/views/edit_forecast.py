import json
import re

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from core.myutils import get_current_financial_year

from costcentre.forms import (
    MyCostCentresForm,
)
from costcentre.models import CostCentre

from forecast.forms import (
    AddForecastRowForm,
    PasteForecastForm,
    PublishForm,
)
from forecast.models import (
    FinancialCode,
    MonthlyFigure,
    MonthlyFigureAmount,
)
from forecast.permission_shortcuts import (
    NoForecastViewPermission,
    get_objects_for_user,
)
from forecast.serialisers import FinancialCodeSerializer
from forecast.utils.edit_helpers import (
    BadFormatException,
    CannotFindMonthlyFigureException,
    NotEnoughMatchException,
    RowMatchException,
    TooManyMatchException,
    check_cols_match,
    check_row_match,
    get_monthly_figures,
)
from forecast.views.base import (
    CostCentrePermissionTest,
    NoCostCentreCodeInURLError,
)


class ChooseCostCentreView(UserPassesTestMixin, FormView):
    template_name = "forecast/edit/choose_cost_centre.html"
    form_class = MyCostCentresForm
    cost_centre = None

    def test_func(self):
        try:
            cost_centres = get_objects_for_user(
                self.request.user,
                "costcentre.change_costcentre",
            )
        except NoForecastViewPermission:
            raise PermissionDenied()

        # If user has permission on
        # one or more CCs then let them view
        return cost_centres.count() > 0

    def get_form_kwargs(self):
        kwargs = super(ChooseCostCentreView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.cost_centre = form.cleaned_data['cost_centre']
        return super(ChooseCostCentreView, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            "edit_forecast",
            kwargs={
                'cost_centre_code': self.cost_centre.cost_centre_code
            }
        )


class AddRowView(CostCentrePermissionTest, FormView):
    template_name = "forecast/edit/add.html"
    form_class = AddForecastRowForm
    cost_centre_code = None

    def get_cost_centre(self):
        if self.cost_centre_code is not None:
            return

        if 'cost_centre_code' not in self.kwargs:
            raise NoCostCentreCodeInURLError(
                "No cost centre code provided in URL"
            )

        self.cost_centre_code = self.kwargs["cost_centre_code"]

    def get_success_url(self):
        self.get_cost_centre()

        return reverse(
            "edit_forecast",
            kwargs={
                'cost_centre_code': self.cost_centre_code
            }
        )

    def cost_centre_details(self):
        self.get_cost_centre()

        cost_centre = CostCentre.objects.get(
            cost_centre_code=self.cost_centre_code,
        )
        return {
            "group": cost_centre.directorate.group.group_name,
            "directorate": cost_centre.directorate.directorate_name,
            "cost_centre_name": cost_centre.cost_centre_name,
            "cost_centre_code": cost_centre.cost_centre_code,
        }

    def form_valid(self, form):
        self.get_cost_centre()
        data = form.cleaned_data

        # TODO - investigate the following statement -
        # "Don't add months that are actuals"
        financial_code = FinancialCode.objects.filter(
            cost_centre_id=self.cost_centre_code,
            programme=data["programme"],
            natural_account_code=data["natural_account_code"],
            analysis1_code=data["analysis1_code"],
            analysis2_code=data["analysis2_code"],
            project_code=data["project_code"],
        ).first()

        if not financial_code:
            financial_code = FinancialCode.objects.create(
                cost_centre_id=self.cost_centre_code,
                programme=data["programme"],
                natural_account_code=data["natural_account_code"],
                analysis1_code=data["analysis1_code"],
                analysis2_code=data["analysis2_code"],
                project_code=data["project_code"],
            )

        for financial_period in range(1, 13):
            monthly_figure = MonthlyFigure.objects.create(
                financial_year_id=get_current_financial_year(),
                financial_period_id=financial_period,
                financial_code=financial_code,
            )

            MonthlyFigureAmount.objects.create(
                amount=0,
                monthly_figure=monthly_figure,
            )

        return super().form_valid(form)


# TODO permission decorator
@require_http_methods(["POST", ])
def pasted_forecast_content(request, cost_centre_code):
    form = PasteForecastForm(
        request.POST,
    )
    if form.is_valid():
        # TODO check user has permission on cost centre
        paste_content = form.cleaned_data['paste_content']
        pasted_at_row = form.cleaned_data.get('pasted_at_row', None)
        all_selected = form.cleaned_data.get('all_selected', False)

        figure_count = MonthlyFigure.objects.filter(
            financial_code__cost_centre_id=cost_centre_code,
        ).count()

        row_count = figure_count / 12

        rows = paste_content.splitlines()

        if len(rows) == 0:
            return JsonResponse({
                'error': 'Your pasted data is not formatted correctly.'
            },
                status=400,
            )

        if all_selected and row_count < len(rows):
            return JsonResponse({
                'error': (
                    'You have selected all forecast rows '
                    'but the pasted data has too many rows.'
                )
            },
                status=400,
            )

        if all_selected and row_count > len(rows):
            return JsonResponse({
                'error': (
                    'You have selected all forecast rows '
                    'but the pasted data has too few rows.'
                )
            },
                status=400,
            )

        # Check for header row
        start_row = 0
        if rows[0] == "Natural Account Code":
            start_row = 1

        monthly_figures = []

        try:
            for index, row in enumerate(rows, start=start_row):
                cell_data = re.split(r'\t', row.rstrip('\t'))

                # Check that pasted at content and desired first row match
                check_row_match(
                    index,
                    pasted_at_row,
                    cell_data,
                )

                # Check cell data length against expected number of cols
                check_cols_match(cell_data)

                row_monthly_figures = get_monthly_figures(
                    cost_centre_code,
                    cell_data,
                )

                monthly_figures.extend(row_monthly_figures)
        except (
                BadFormatException,
                TooManyMatchException,
                NotEnoughMatchException,
                RowMatchException,
                CannotFindMonthlyFigureException,
        ) as ex:
            return JsonResponse({
                'error': str(ex)
            },
                status=400,
            )

        # Update monthly figures
        for monthly_figure in monthly_figures:
            monthly_figure_amount = MonthlyFigureAmount.objects.filter(
                monthly_figure=monthly_figure,
            ).order_by(
                "-version"
            ).first()
            monthly_figure_amount.version = monthly_figure_amount.version + 1
            monthly_figure_amount.save()

        financial_code = FinancialCode.objects.filter(
            cost_centre_id=cost_centre_code,
        )

        financial_code_serialiser = FinancialCodeSerializer(
            financial_code,
            many=True,
        )

        return JsonResponse(financial_code_serialiser.data, safe=False)
    else:
        return JsonResponse({
            'error': 'There was a problem with your '
                     'submission, please contact support'
        },
            status=400,
        )


class EditForecastView(
    CostCentrePermissionTest,
    TemplateView,
):
    template_name = "forecast/edit/edit.html"

    def cost_centre_details(self):
        return {
            "group": "Test group",
            "directorate": "Test directorate",
            "cost_centre_name": "Test cost centre name",
            "cost_centre_code": self.cost_centre_code,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = PublishForm(
            initial={
                "cost_centre_code": self.cost_centre_code,
            }
        )

        financial_code = FinancialCode.objects.filter(
            cost_centre_id=self.cost_centre_code,
        )

        financial_code_serialiser = FinancialCodeSerializer(
            financial_code,
            many=True,
        )

        forecast_dump = json.dumps(financial_code_serialiser.data)
        paste_form = PasteForecastForm()

        context["form"] = form
        context["paste_form"] = paste_form
        context["forecast_dump"] = forecast_dump
        return context
