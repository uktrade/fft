from .tables import CostCentreTable, ProgrammeTable
from .filters import CostCentreFilter, ProgrammeFilter
from core.views import FAdminFilteredView


class FilteredCostListView(FAdminFilteredView):
    table_class = CostCentreTable
    model = table_class.Meta.model
    filterset_class = CostCentreFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Cost Centre Hierarchy'
        return context


class FilteredProgrammeView(FAdminFilteredView):
    table_class = ProgrammeTable
    model = table_class.Meta.model
    filterset_class = ProgrammeFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Programme Codes'
        return context


