from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import TemplateView
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin, TableExport
from django_tables2.views import SingleTableMixin

from core.utils.export_helpers import EXC_TAB_NAME_LEN
from core.utils.generic_helpers import (
    get_current_financial_year,
    get_year_display,
    today_string,
)


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
