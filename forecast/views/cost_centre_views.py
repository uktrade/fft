from django.urls import reverse
from django.views.generic.edit import FormView

from costcentre.forms import ChooseCostCentreForm


class ChooseCostCentreView(FormView):
    template_name = "forecast/choose_cost_centre.html"
    form_class = ChooseCostCentreForm
    cost_centre_code = None

    def get_success_url(self):
        cost_centre_code = self.request.POST.get(
            'cost_centre',
            None,
        )
        if cost_centre_code:
            return reverse(
                "edit_forecast",
                kwargs={'cost_centre_code': cost_centre_code}
            )

        return None
