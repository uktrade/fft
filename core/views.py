from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin, TableExport
from django_tables2.views import SingleTableMixin


@login_required()
def index(request):
    return render(
        request, 'core/index.html'
    )


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


class FAdminFilteredView(FidoExportMixin, SingleTableMixin, FilterView):
    paginate_by = 200
    template_name = 'core/table_filter_generic.html'
    strict = False
    sheet_name = 'Chart of Account'
