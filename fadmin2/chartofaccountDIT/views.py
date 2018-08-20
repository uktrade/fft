
from core.views import FAdminFilteredView


from .tables import NaturalCodeTable
from .filters import NACFilter


class FilteredNACListView(FAdminFilteredView):
    table_class = NaturalCodeTable
    model = table_class.Meta.model
    filterset_class = NACFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Natural Account Codes (NAC)'
        return context

