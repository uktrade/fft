from core.utils import today_string

from core.views import FAdminFilteredView

from django.contrib.auth.mixins import LoginRequiredMixin

from .filters import CostCentreFilter
from .tables import CostCentreTable


class FilteredCostListView(LoginRequiredMixin, FAdminFilteredView):
    table_class = CostCentreTable
    model = table_class.Meta.model
    filterset_class = CostCentreFilter
    export_name = 'Cost Centre Hierarchy' + today_string()
    sheet_name = 'Cost Centre Hierarchy'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Cost Centre Hierarchy'
        context['section_description'] = 'This field reflects our organisational structure which enables ' \
                                 'us to report and produce Financial MI. A cost centre is an ' \
                                 'identifiable unit of an organisation whose managers ' \
                                 '(usually Deputy Director or above) are responsible for all ' \
                                 'its associated costs and for ensuring adherence to budgets. '
        return context
