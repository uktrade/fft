import json
import re

from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
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
    EditForm,
    PasteForecastForm,
    UploadActualsForm,
)
from forecast.models import (
    FinancialPeriod,
    MonthlyFigure,
)
from forecast.permission_shortcuts import (
    NoForecastViewPermission,
    get_objects_for_user,
)
from forecast.tasks import process_uploaded_file
from forecast.utils import (
    CannotFindMonthlyFigureException,
    ColMatchException,
    RowMatchException,
    check_cols_match,
    check_row_match,
    get_forecast_monthly_figures_pivot,
    get_monthly_figures,
)
from forecast.views.base import (
    CostCentrePermissionTest,
    NoCostCentreCodeInURLError,
)

from upload_file.decorators import has_upload_permission
from upload_file.models import FileUpload


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
        for financial_period in range(1, 13):
            monthly_figure = MonthlyFigure(
                financial_year_id=get_current_financial_year(),
                financial_period_id=financial_period,
                cost_centre_id=self.cost_centre_code,
                programme=data["programme"],
                natural_account_code=data["natural_account_code"],
                analysis1_code=data["analysis1_code"],
                analysis2_code=data["analysis2_code"],
                project_code=data["project_code"],
                amount=0,
            )
            monthly_figure.save()

        return super().form_valid(form)


class UploadActualsView(FormView):
    template_name = "forecast/file_upload.html"
    form_class = UploadActualsForm
    success_url = reverse_lazy("uploaded_files")

    @has_upload_permission
    def dispatch(self, *args, **kwargs):
        return super(UploadActualsView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            data = form.cleaned_data

            file_upload = FileUpload(
                document_file=request.FILES['file'],
                uploading_user=request.user,
            )
            file_upload.save()
            # Process file async

            if settings.ASYNC_FILE_UPLOAD:
                process_uploaded_file.delay(
                    data['period'].period_calendar_code,
                    data['year'].financial_year,
                )
            else:
                process_uploaded_file(
                    data['period'].period_calendar_code,
                    data['year'].financial_year,
                )

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


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

        forecast_dump = get_forecast_monthly_figures_pivot(
            cost_centre_code
        )

        rows = paste_content.splitlines()

        if all_selected and len(forecast_dump) != len(rows):
            return JsonResponse({
                'error': 'Your pasted data does not match the selected rows.'
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
                ColMatchException,
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
            monthly_figure.save()

        forecast_dump = get_forecast_monthly_figures_pivot(
            cost_centre_code
        )

        return JsonResponse(forecast_dump, safe=False)
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

        form = EditForm(
            initial={
                "financial_year": get_current_financial_year(),
                "cost_centre_code": self.cost_centre_code,
            }
        )

        pivot_filter = {"cost_centre__cost_centre_code": "{}".format(
            self.cost_centre_code
        )}
        monthly_figures = MonthlyFigure.pivot.pivot_data({}, pivot_filter)

        # TODO - Luisella to restrict to financial year
        actuals_periods = list(FinancialPeriod.objects.filter(actual_loaded=True).all())
        actuals_periods_dump = serializers.serialize("json", actuals_periods)
        forecast_dump = json.dumps(list(monthly_figures), cls=DjangoJSONEncoder)
        paste_form = PasteForecastForm()

        context["form"] = form
        context["paste_form"] = paste_form
        context["actuals_periods_dump"] = actuals_periods_dump
        context["forecast_dump"] = forecast_dump
        return context

    def post(self):
        form = EditForm(self.request.POST)
        if form.is_valid():
            cost_centre_code = form.cleaned_data["cost_centre_code"]
            financial_year = form.cleaned_data["financial_year"]

            cell_data = json.loads(form.cleaned_data["cell_data"])

            for key, cell in cell_data.items():
                if cell["editable"]:
                    monthly_figure = MonthlyFigure.objects.filter(
                        cost_centre__cost_centre_code=cost_centre_code,
                        financial_year__financial_year=financial_year,
                        financial_period__period_short_name__iexact=cell["key"],
                        programme__programme_code=cell["programmeCode"],
                        natural_account_code__natural_account_code=cell[
                            "naturalAccountCode"
                        ],
                    ).first()
                    monthly_figure.amount = int(float(cell["value"]))
                    monthly_figure.save()
