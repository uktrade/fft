from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django_filters.views import FilterView

from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin


@login_required()
def index(request):
    return render(
        request, 'core/index.html'
    )


class FAdminFilteredView(ExportMixin, SingleTableMixin, FilterView):
    paginate_by = 200
    template_name = 'core/table_filter_generic.html'
    strict = False
