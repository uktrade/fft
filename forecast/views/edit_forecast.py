import json
import logging
import re
from functools import cached_property

from django.conf import settings
from django.db import transaction
from django.db.models import Exists, OuterRef, Prefetch, Q, Sum
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from core.models import FinancialYear
from core.utils.generic_helpers import get_current_financial_year, get_year_display
from costcentre.models import CostCentre
from forecast.forms import (
    AddForecastRowForm,
    EditForecastFigureForm,
    PasteForecastForm,
    PublishForm,
)
from forecast.models import (
    BudgetMonthlyFigure,
    FinancialCode,
    FinancialPeriod,
    ForecastMonthlyFigure,
)
from forecast.serialisers import FinancialCodeSerializer
from forecast.utils.access_helpers import (
    can_forecast_be_edited,
    can_future_forecast_be_edited,
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
    NoFinancialYearInURLError,
)


UNAVAILABLE_FORECAST_EDIT_TITLE = "Forecast editing is locked"
UNAVAILABLE_FUTURE_FORECAST_EDIT_TITLE = "Future forecast editing is locked"
UNAVAILABLE_FORECAST_EDIT_MESSAGE = "Editing is unavailable until month end processing has been completed."  # noqa: E501
UNAVAILABLE_FUTURE_FORECAST_EDIT_MESSAGE = (
    "Editing future years forecast is not available at the moment."  # noqa: E501
)


def get_financial_codes_for_year(cost_centre_code, financial_year):
    # Only selects the financial codes relevant to the financial year being edited.
    # Financial codes are used in budgets and forecast/actuals.
    forecasts = ForecastMonthlyFigure.objects.filter(
        financial_year_id=financial_year,
        archived_status__isnull=True,
    )
    budgets = BudgetMonthlyFigure.objects.filter(
        financial_year_id=financial_year,
        archived_status__isnull=True,
    )
    return FinancialCode.objects.filter(cost_centre_id=cost_centre_code).filter(
        Q(Exists(forecasts.filter(financial_code_id=OuterRef("pk"))))
        | Q(Exists(budgets.filter(financial_code_id=OuterRef("pk"))))
    )


def get_financial_code_serialiser(
    cost_centre_code: str,
    financial_year: FinancialYear,
    current_financial_year: FinancialYear | None,
) -> FinancialCodeSerializer:
    if current_financial_year is None:
        current_financial_year = get_current_financial_year()

    # Only selects the financial codes relevant to the financial year being edited.
    # Financial codes are used in budgets and forecast/actuals.
    forecasts = ForecastMonthlyFigure.objects.select_related("financial_period").filter(
        financial_year_id=financial_year,
        archived_status__isnull=True,
    )
    financial_codes = (
        get_financial_codes_for_year(cost_centre_code, financial_year)
        .select_related("programme", "natural_account_code", "cost_centre")
        .prefetch_related(
            Prefetch(
                "forecast_forecastmonthlyfigures",
                queryset=forecasts,
                to_attr="monthly_figure_items",
            ),
        )
        .annotate(
            yearly_budget_amount=Sum(
                "forecast_budgetmonthlyfigures__amount",
                filter=Q(
                    forecast_budgetmonthlyfigures__financial_year_id=financial_year,
                    forecast_budgetmonthlyfigures__archived_status=None,
                ),
                default=0,
            )
        )
        .order_by(*edit_forecast_order())
    )

    financial_code_serialiser = FinancialCodeSerializer(
        financial_codes,
        many=True,
        context={
            "financial_year": financial_year,
            "current_financial_year": current_financial_year,
        },
    )
    return financial_code_serialiser


logger = logging.getLogger(__name__)


class AddRowView(
    CostCentrePermissionTest,
    FormView,
):
    template_name = "forecast/edit/add.html"
    form_class = AddForecastRowForm
    cost_centre_code = None

    def get_cost_centre_and_year(self):
        if self.cost_centre_code is not None:
            return

        if "cost_centre_code" not in self.kwargs:
            raise NoCostCentreCodeInURLError("No cost centre code provided in URL")

        self.cost_centre_code = self.kwargs["cost_centre_code"]

        if "financial_year" not in self.kwargs:
            raise NoFinancialYearInURLError("No financial year provided in URL")

        self.financial_year = self.kwargs["financial_year"]

    def get_success_url(self):
        self.get_cost_centre_and_year()

        if self.financial_year == get_current_financial_year():
            return reverse(
                "edit_forecast", kwargs={"cost_centre_code": self.cost_centre_code}
            )
        return reverse(
            "edit_forecast",
            kwargs={
                "cost_centre_code": self.cost_centre_code,
                "financial_year": self.financial_year,
            },
        )

    def cost_centre_details(self):
        self.get_cost_centre_and_year()

        cost_centre = CostCentre.objects.get(
            cost_centre_code=self.cost_centre_code,
        )
        return {
            "group": cost_centre.directorate.group.group_name,
            "group_code": cost_centre.directorate.group.group_code,
            "directorate": cost_centre.directorate.directorate_name,
            "directorate_code": cost_centre.directorate.directorate_code,
            "cost_centre_name": cost_centre.cost_centre_name,
            "cost_centre_code": cost_centre.cost_centre_code,
        }

    def get_form_kwargs(self):
        self.get_cost_centre_and_year()

        kwargs = super(AddRowView, self).get_form_kwargs()
        kwargs["cost_centre_code"] = self.cost_centre_code
        kwargs["financial_year"] = self.financial_year
        return kwargs

    def form_valid(self, form):
        data = form.cleaned_data

        financial_code, _ = FinancialCode.objects.get_or_create(
            cost_centre_id=self.cost_centre_code,
            programme=data["programme"],
            natural_account_code=data["natural_account_code"],
            analysis1_code=data["analysis1_code"],
            analysis2_code=data["analysis2_code"],
            project_code=data["project_code"],
        )

        # Create "actual" monthly figures for past months, otherwise some of the
        # queries used to view the forecast will fail.
        actual_months = FinancialPeriod.financial_period_info.actual_period_code_list()

        if (
            self.financial_year == get_current_financial_year()
            and len(actual_months) > 0
        ):
            for actual_month in actual_months:
                ForecastMonthlyFigure.objects.get_or_create(
                    financial_code=financial_code,
                    financial_year_id=self.financial_year,
                    financial_period_id=actual_month,
                )
        else:
            # Create at least one entry, to help some of the queries used to view
            # the forecast
            ForecastMonthlyFigure.objects.get_or_create(
                financial_code=financial_code,
                financial_year_id=self.financial_year,
                financial_period_id=1,
                archived_status=None,
            )

        return super().form_valid(form)


class PasteForecastRowsView(
    CostCentrePermissionTest,
    FormView,
):
    form_class = PasteForecastForm

    @transaction.atomic
    def form_valid(self, form):  # noqa: C901
        if "cost_centre_code" not in self.kwargs:
            raise NoCostCentreCodeInURLError("No cost centre code provided in URL")

        try:
            cost_centre_code = self.kwargs["cost_centre_code"]

            paste_content = form.cleaned_data["paste_content"]
            pasted_at_row = form.cleaned_data.get("pasted_at_row", None)
            all_selected = form.cleaned_data.get("all_selected", False)

            financial_codes = get_financial_codes_for_year(
                cost_centre_code, self.financial_year
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
                        index,
                        pasted_at_row,
                        cell_data,
                    )

                    # Check cell data length against expected number of cols
                    check_cols_match(cell_data)

                    set_monthly_figure_amount(
                        cost_centre_code, cell_data, self.financial_year
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
                return JsonResponse(
                    {"error": str(ex)},
                    status=400,
                )

            financial_code_serialiser = get_financial_code_serialiser(
                self.cost_centre_code,
                self.financial_year,
                self.request.current_financial_year,
            )

            return JsonResponse(
                financial_code_serialiser.data,
                safe=False,
            )
        except Exception as ex:
            logger.fatal(
                f"Error when pasting forecast data {ex}",
                exc_info=True,
            )
            return JsonResponse(
                {
                    "error": "There was an error when attempting to paste "
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
    CostCentrePermissionTest,
    FormView,
):
    form_class = EditForecastFigureForm

    def form_valid(self, form):
        if "cost_centre_code" not in self.kwargs:
            raise NoCostCentreCodeInURLError("No cost centre code provided in URL")

        if "financial_year" not in self.kwargs:
            raise NoFinancialYearInURLError("No financial year provided in URL")

        cost_centre_code = self.kwargs["cost_centre_code"]

        cost_centre = CostCentre.objects.filter(
            cost_centre_code=cost_centre_code,
        ).first()

        financial_year = self.kwargs["financial_year"]

        financial_code = FinancialCode.objects.filter(
            cost_centre=cost_centre,
            natural_account_code=form.cleaned_data["natural_account_code"],
            programme__programme_code=form.cleaned_data["programme_code"],
            analysis1_code__analysis1_code=form.cleaned_data.get(
                "analysis1_code",
                None,
            ),
            analysis2_code__analysis2_code=form.cleaned_data.get(
                "analysis2_code",
                None,
            ),
            project_code__project_code=form.cleaned_data.get(
                "project_code",
                None,
            ),
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

        financial_code_serialiser = get_financial_code_serialiser(
            self.cost_centre_code,
            self.financial_year,
            self.request.current_financial_year,
        )

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
    CostCentrePermissionTest,
    TemplateView,
):
    template_name = "forecast/edit/edit.html"
    _future_year_display = None

    def class_name(self):
        return "wide-table"

    @cached_property
    def cost_centre_details(self):
        cost_centre = CostCentre.objects.select_related("directorate__group").get(
            cost_centre_code=self.cost_centre_code,
        )
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

        form = PublishForm(
            initial={
                "cost_centre_code": self.cost_centre_code,
            }
        )
        financial_code_serialiser = get_financial_code_serialiser(
            self.cost_centre_code,
            self.financial_year,
            self.request.current_financial_year,
        )
        serialiser_data = financial_code_serialiser.data
        forecast_dump = json.dumps(serialiser_data)

        if self.financial_year == self.request.current_financial_year:
            self.title = "Edit forecast"
            actual_data = (
                FinancialPeriod.financial_period_info.actual_period_code_list()
            )
        else:
            actual_data = []
            self.title = f"Edit future forecast: {self.future_year_display}"
        period_display = (
            FinancialPeriod.financial_period_info.period_display_code_list()
        )
        paste_form = PasteForecastForm()

        context["form"] = form
        context["paste_form"] = paste_form
        context["forecast_dump"] = forecast_dump
        context["actuals"] = actual_data
        context["period_display"] = period_display

        return context

    @cached_property
    def future_year_display(self):
        if self._future_year_display is None:
            current_year = self.request.current_financial_year
            if self.financial_year > current_year:
                self._future_year_display = get_year_display(self.financial_year)
            else:
                self._future_year_display = ""
        return self._future_year_display


class EditUnavailableView(
    TemplateView,
):
    template_name = "forecast/edit/edit_locked.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        financial_year = kwargs["financial_year"]
        if financial_year == get_current_financial_year():
            context["title"] = UNAVAILABLE_FORECAST_EDIT_TITLE
            context["message"] = UNAVAILABLE_FORECAST_EDIT_MESSAGE

        else:
            context["title"] = UNAVAILABLE_FUTURE_FORECAST_EDIT_TITLE
            context["message"] = UNAVAILABLE_FUTURE_FORECAST_EDIT_MESSAGE
        return context

    def dispatch(self, request, *args, **kwargs):
        # If edit is open, redirect to choose CC page
        if can_forecast_be_edited(request.user) or can_future_forecast_be_edited(
            request.user
        ):
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
        return 1 / 0
