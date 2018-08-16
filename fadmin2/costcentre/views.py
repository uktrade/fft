
from django_tables2.export.views import ExportMixin

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from .models import  CostCentre

from .tables import CostCentreTable
from .filters import CostCentreFilter


class FilteredCostListView(ExportMixin, SingleTableMixin, FilterView):
    table_class = CostCentreTable
    model = CostCentre
    paginate_by = 50
    template_name = 'core/table_filter_generic.html'
    filterset_class = CostCentreFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Cost Centres'
        return context


