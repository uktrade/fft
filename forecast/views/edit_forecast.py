import json
import logging
import re

from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import (
    reverse,
)
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from core.utils.generic_helpers import get_current_financial_year

from costcentre.forms import MyCostCentresForm
from costcentre.models import CostCentre

from forecast.forms import (
    AddForecastRowForm,
    EditForecastFigureForm,
    PasteForecastForm,
    PublishForm,
)
from forecast.models import (
    FinancialCode,
    FinancialPeriod,
    ForecastMonthlyFigure,
)
from forecast.serialisers import FinancialCodeSerializer
from forecast.utils.access_helpers import (
    can_edit_at_least_one_cost_centre,
    can_forecast_be_edited,
    get_user_cost_centres,
)
from forecast.utils.edit_helpers import (
    BadFormatException,
    CannotFindForecastMonthlyFigureException,
    CannotFindMonthlyFigureException,
    IncorrectDecimalFormatException,
    NoFinancialCodeForEditedValue,
    NotEnoughColumnsException,
    NotEnoughMatchException,
    RowMatchException,
    TooManyMatchException,
    check_cols_match,
    check_row_match,
    set_monthly_figure_amount,
)
from forecast.utils.query_fields import edit_forecast_order
from forecast.views.base import (
    CostCentrePermissionTest,
    NoCostCentreCodeInURLError,
)


def get_financial_code_serialiser(cost_centre_code):
    financial_codes = (
        FinancialCode.objects.filter(cost_centre_id=cost_centre_code, )
        .prefetch_related(
            "forecast_forecastmonthlyfigures",
            "forecast_forecastmonthlyfigures__financial_period",
        ).order_by(*edit_forecast_order())
    )

    return FinancialCodeSerializer(financial_codes, many=True, )


logger = logging.getLogger(__name__)


class ChooseCostCentreView(
    UserPassesTestMixin,
    FormView,
):
    template_name = "forecast/edit/choose_cost_centre.html"
    form_class = MyCostCentresForm
    cost_centre = None

    def test_func(self):
        can_edit = can_edit_at_least_one_cost_centre(
            self.request.user
        )

        if not can_edit:
            raise PermissionDenied()

        return True

    def get_user_cost_centres(self):
        user_cost_centres = get_user_cost_centres(
            self.request.user,
        )

        cost_centres = []

        for (cost_centre) in user_cost_centres:
            cost_centres.append({
                "name": cost_centre.cost_centre_name,
                "code": cost_centre.cost_centre_code,
            })

        return json.dumps(cost_centres)

    def get_form_kwargs(self):
        kwargs = super(ChooseCostCentreView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.cost_centre = form.cleaned_data["cost_centre"]
        return super(ChooseCostCentreView, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            "edit_forecast",
            kwargs={"cost_centre_code": self.cost_centre.cost_centre_code},
        )


class AddRowView(
    CostCentrePermissionTest, FormView,
):
    template_name = "forecast/edit/add.html"
    form_class = AddForecastRowForm
    cost_centre_code = None

    def get_cost_centre(self):
        if self.cost_centre_code is not None:
            return

        if "cost_centre_code" not in self.kwargs:
            raise NoCostCentreCodeInURLError("No cost centre code provided in URL")

        self.cost_centre_code = self.kwargs["cost_centre_code"]

    def get_success_url(self):
        self.get_cost_centre()

        return reverse(
            "edit_forecast", kwargs={"cost_centre_code": self.cost_centre_code}
        )

    def cost_centre_details(self):
        self.get_cost_centre()

        cost_centre = CostCentre.objects.get(cost_centre_code=self.cost_centre_code,)
        return {
            "group": cost_centre.directorate.group.group_name,
            "group_code": cost_centre.directorate.group.group_code,
            "directorate": cost_centre.directorate.directorate_name,
            "directorate_code": cost_centre.directorate.directorate_code,
            "cost_centre_name": cost_centre.cost_centre_name,
            "cost_centre_code": cost_centre.cost_centre_code,
        }

    def get_form_kwargs(self):
        self.get_cost_centre()

        kwargs = super(AddRowView, self).get_form_kwargs()
        kwargs['cost_centre_code'] = self.cost_centre_code
        return kwargs

    def form_valid(self, form):
        data = form.cleaned_data

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

        # Create "actual" monthly figures for past months
        actual_months = FinancialPeriod.financial_period_info.actual_period_code_list()

        if len(actual_months) > 0:
            financial_year = get_current_financial_year()

            for actual_month in actual_months:
                ForecastMonthlyFigure.objects.create(
                    financial_code=financial_code,
                    financial_year_id=financial_year,
                    financial_period_id=actual_month,
                )

        return super().form_valid(form)


class PasteForecastRowsView(
    CostCentrePermissionTest, FormView,
):
    form_class = PasteForecastForm

    @transaction.atomic  # noqa: C901
    def form_valid(self, form):
        if "cost_centre_code" not in self.kwargs:
            raise NoCostCentreCodeInURLError("No cost centre code provided in URL")

        try:
            cost_centre_code = self.kwargs["cost_centre_code"]

            paste_content = form.cleaned_data["paste_content"]
            pasted_at_row = form.cleaned_data.get("pasted_at_row", None)
            all_selected = form.cleaned_data.get("all_selected", False)

            financial_codes = FinancialCode.objects.filter(
                cost_centre_id=self.cost_centre_code,
            )

            # TODO - introduce a way of checking for
            # active financial periods (see previously used logic below)

            # Get number of active financial periods
            # active_periods = FinancialPeriod.objects.filter(
            #     display_figure=True
            # ).count()

            row_count = financial_codes.count()
            rows = paste_content.splitlines()

            # Remove any rows that start with empty cells (to account for totals etc)
            rows = [row for row in rows if not row[0].strip() == ""]

            pasted_row_count = len(rows)

            if len(rows) == 0:
                return JsonResponse(
                    {"error": "Your pasted data is not formatted correctly."},
                    status=400,
                )

            # Check for header row
            has_start_row = False
            if rows[0].lower().startswith("programme"):
                has_start_row = True

            # Account for header row in paste
            if has_start_row:
                pasted_row_count -= 1

            if all_selected and row_count < pasted_row_count:
                return JsonResponse(
                    {
                        "error": (
                            "You have selected all forecast rows "
                            "but the pasted data has too many rows."
                        )
                    },
                    status=400,
                )

            if all_selected and row_count > pasted_row_count:
                return JsonResponse(
                    {
                        "error": (
                            "You have selected all forecast rows "
                            "but the pasted data has too few rows."
                        )
                    },
                    status=400,
                )

            try:
                for index, row in enumerate(rows):
                    if index == 0 and has_start_row:
                        continue

                    cell_data = re.split(r"\t", row.rstrip("\t"))

                    # Check that pasted at content and desired first row match
                    check_row_match(
                        index, pasted_at_row, cell_data,
                    )

                    # Check cell data length against expected number of cols
                    check_cols_match(cell_data)

                    set_monthly_figure_amount(
                        cost_centre_code, cell_data,
                    )
            except (
                BadFormatException,
                TooManyMatchException,
                NotEnoughColumnsException,
                NotEnoughMatchException,
                RowMatchException,
                CannotFindMonthlyFigureException,
                CannotFindForecastMonthlyFigureException,
                IncorrectDecimalFormatException,
            ) as ex:
                return JsonResponse({"error": str(ex)}, status=400,)

            financial_code_serialiser = get_financial_code_serialiser(
                self.cost_centre_code,
            )

            return JsonResponse(
                financial_code_serialiser.data,
                safe=False,
            )
        except Exception:
            logger.fatal(
                "Error when pasting forecast data",
                exc_info=True,
            )
            return JsonResponse(
                {"error": "There was an error when attempting to paste "
                          "your data, please make sure you have selected "
                          "all columns when you copy from the spreadsheet. "
                          "Some of the forecast data may have been updated. "
                          "If the error persists, please contact the Live "
                          "Services Team"
                 },
                status=400,
            )

    def form_invalid(self, form):
        return JsonResponse(
            {
                "error": "There was a problem with your "
                "submission, please contact support"
            },
            status=400,
        )


class EditForecastFigureView(
    CostCentrePermissionTest, FormView,
):
    form_class = EditForecastFigureForm

    def form_valid(self, form):
        if "cost_centre_code" not in self.kwargs:
            raise NoCostCentreCodeInURLError("No cost centre code provided in URL")

        cost_centre_code = self.kwargs["cost_centre_code"]

        cost_centre = CostCentre.objects.filter(
            cost_centre_code=cost_centre_code,
        ).first()

        financial_year = get_current_financial_year()

        financial_code = FinancialCode.objects.filter(
            cost_centre=cost_centre,
            natural_account_code=form.cleaned_data["natural_account_code"],
            programme__programme_code=form.cleaned_data["programme_code"],
            analysis1_code__analysis1_code=form.cleaned_data.get(
                "analysis1_code", None,
            ),
            analysis2_code__analysis2_code=form.cleaned_data.get(
                "analysis2_code", None,
            ),
            project_code__project_code=form.cleaned_data.get("project_code", None,),
        )

        month = form.cleaned_data["month"]

        if not financial_code.first():
            raise NoFinancialCodeForEditedValue()

        monthly_figure = ForecastMonthlyFigure.objects.filter(
            financial_year_id=financial_year,
            financial_code=financial_code.first(),
            financial_period__financial_period_code=month,
            archived_status=None,
        ).first()

        amount = form.cleaned_data["amount"]

        if amount > settings.MAX_FORECAST_FIGURE:
            amount = settings.MAX_FORECAST_FIGURE

        if amount < settings.MIN_FORECAST_FIGURE:
            amount = settings.MIN_FORECAST_FIGURE

        if monthly_figure:
            monthly_figure.amount = amount
        else:
            financial_period = FinancialPeriod.objects.filter(
                financial_period_code=month
            ).first()
            monthly_figure = ForecastMonthlyFigure(
                financial_year_id=financial_year,
                financial_code=financial_code.first(),
                financial_period=financial_period,
                amount=amount,
            )

        monthly_figure.save()

        financial_code_serialiser = get_financial_code_serialiser(self.cost_centre_code)

        return JsonResponse(financial_code_serialiser.data, safe=False)

    def form_invalid(self, form):
        return JsonResponse(
            {
                "error": "There was a problem with your "
                "submission, please contact support"
            },
            status=400,
        )


class EditForecastView(
    CostCentrePermissionTest, TemplateView,
):
    template_name = "forecast/edit/edit.html"

    def class_name(self):
        return "wide-table"

    def cost_centre_details(self):
        cost_centre = CostCentre.objects.get(cost_centre_code=self.cost_centre_code,)
        return {
            "group": cost_centre.directorate.group.group_name,
            "group_code": cost_centre.directorate.group.group_code,
            "directorate": cost_centre.directorate.directorate_name,
            "directorate_code": cost_centre.directorate.directorate_code,
            "cost_centre_name": cost_centre.cost_centre_name,
            "cost_centre_code": cost_centre.cost_centre_code,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = PublishForm(initial={"cost_centre_code": self.cost_centre_code, })

        financial_code_serialiser = get_financial_code_serialiser(
            self.cost_centre_code,
        )

        serialiser_data = financial_code_serialiser.data
        forecast_dump = json.dumps(serialiser_data)

        actual_data = FinancialPeriod.financial_period_info.actual_period_code_list()
        period_display = (
            FinancialPeriod.financial_period_info.period_display_code_list()
        )  # noqa
        paste_form = PasteForecastForm()

        context["form"] = form
        context["paste_form"] = paste_form
        context["forecast_dump"] = forecast_dump
        context["actuals"] = actual_data
        context["period_display"] = period_display

        return context


class EditUnavailableView(
    TemplateView,
):
    template_name = "forecast/edit/edit_locked.html"

    def dispatch(self, request, *args, **kwargs):
        # If edit is open, redirect to choose CC page
        if can_forecast_be_edited(request.user):
            return redirect(reverse("choose_cost_centre"))

        return super(EditUnavailableView, self).dispatch(
            request,
            *args,
            **kwargs,
        )


class ErrorView(
    TemplateView,
):
    def dispatch(self, request, *args, **kwargs):
        1 / 0
