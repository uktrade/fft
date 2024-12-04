from functools import wraps
import datetime as dt
import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import TemplateView
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin, TableExport
from django_tables2.views import SingleTableMixin
from django.core.exceptions import PermissionDenied
from django.db.models.functions import Coalesce, Concat
from django.db.models import Sum, Value, Q, F
from django.db import models

from core.utils.export_helpers import EXC_TAB_NAME_LEN
from core.utils.generic_helpers import (
    get_current_financial_year,
    get_year_display,
    today_string,
)
from forecast.models import BudgetMonthlyFigure, FinancialPeriod


@login_required()
def index(request):
    return render(request, "core/index.html")


class TableExportWithSheetName(TableExport):
    def __init__(self, sheet_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dataset.title = sheet_name


class FidoExportMixin(ExportMixin):
    def create_export(self, export_format):
        exporter = TableExportWithSheetName(
            export_format=export_format,
            table=self.get_table(**self.get_table_kwargs()),
            exclude_columns=self.exclude_columns,
            sheet_name=self.sheet_name,
        )

        return exporter.response(filename=self.get_export_filename(export_format))


class FAdminFilteredView(
    FidoExportMixin,
    SingleTableMixin,
    FilterView,
):
    def display_year(self):
        return get_current_financial_year()

    paginate_by = 200
    template_name = "core/table_filter_generic.html"
    strict = False
    name = "View"

    def class_name(self):
        return "wide-table"

    def get_table_kwargs(self):
        return {
            "template_name": "django_tables_2_bootstrap.html",
            "attrs": {
                "class": "govuk-table finance-table",
                "thead": {"class": "govuk-table__head"},
                "tbody": {"class": "govuk-table__body"},
                "th": {"class": "govuk-table__header", "a": {"class": "govuk-link"}},
                "td": {"class": "govuk-table__cell", "a": {"class": "govuk-link"}},
                "a": {"class": "govuk-link"},
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Define the export name at init,
        # so it uses the current date, and
        # not the date the class was loaded
        # for the first time
        self.export_name = self.name + " " + today_string()
        # The max length for an Excel tab name is 31.
        # So truncate the name, if needed
        self.sheet_name = self.name[:EXC_TAB_NAME_LEN]


class HistoricalFilteredView(FAdminFilteredView):
    def display_year(self):
        return int(self.filterset_class.year)

    def get(self, request, *args, **kwargs):
        year = kwargs["year"]
        self.filterset_class.year = year
        year_display = get_year_display(year)
        self.name = f"{self.name} {year_display}"
        return super().get(request, *args, **kwargs)


class AccessibilityPageView(TemplateView):
    template_name = "core/accessibility_statement.html"


def logout(request):
    if request.method == "POST":
        logout(request)

    return redirect(reverse("index"))


def report_view(func):
    @wraps(func)
    def view(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.user.is_superuser:
            raise PermissionDenied

        report_name, header, results = func(request, *args, **kwargs)

        filename = f"{report_name}_{dt.datetime.now():%Y%m%d-%H%M%S}.csv"
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

        writer = csv.writer(response)
        writer.writerow(header)
        for result in results:
            writer.writerow(result)

        return response

    return view


@report_view
def budget_report(request: HttpRequest, *args, **kwargs):
    periods = FinancialPeriod.objects.all()

    key_fields = [
        "financial_code__cost_centre__cost_centre_code",
        "financial_code__natural_account_code__natural_account_code",
        "financial_code__programme__programme_code",
        "financial_code__analysis1_code__analysis1_code",
        "financial_code__analysis2_code__analysis2_code",
        "financial_code__project_code__project_code",
    ]

    budget_per_month_annotation = {
        period.period_short_name: Sum(
            "amount", filter=Q(financial_period_id=period.pk), default=0
        )
        / 100
        for period in periods
    }

    qs = (
        BudgetMonthlyFigure.objects.select_related("financial_code")
        .filter(
            archived_status__isnull=True,
            financial_year=request.current_financial_year,
        )
        .annotate(key=Concat(*key_fields, output_field=models.CharField()))
        .values_list("key", *key_fields)
        .annotate(
            **budget_per_month_annotation | dict(total=Sum("amount", default=0) / 100),
        )
    )

    header = [
        "Key",
        "Cost Centre",
        "Natural Account",
        "Programme",
        "Analysis",
        "Analysis2",
        "Project",
        *[period.period_short_name for period in periods],
        "Total",
    ]

    return "budget-report", header, qs
