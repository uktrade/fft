import json
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import FormView
from django.urls import reverse

from core.models import FinancialYear
from core.utils.generic_helpers import get_current_financial_year

from costcentre.forms import MyCostCentresForm, MyCostCentresYearForm

# from forecast.forms import ForecastFutureYearForm
from forecast.utils.access_helpers import (
    can_edit_at_least_one_cost_centre,
    get_user_cost_centres,
)


class ChooseCostCentreView(
    UserPassesTestMixin,
    FormView,
):
    template_name = "forecast/edit/choose_cost_centre.html"
    form_class = MyCostCentresForm
    cost_centre = None

    def test_func(self):
        can_edit = can_edit_at_least_one_cost_centre(
            self.request.user
        )

        if not can_edit:
            raise PermissionDenied()

        return True

    def get_financial_year(self):
        return get_current_financial_year()


    def get_user_cost_centres(self):
        user_cost_centres = get_user_cost_centres(
            self.request.user,
        )

        cost_centres = []
        financial_year = self.get_financial_year()
        for (cost_centre) in user_cost_centres:
            cost_centres.append({
                "name": cost_centre.cost_centre_name,
                "code": cost_centre.cost_centre_code,
                "year": financial_year,
            })

        return json.dumps(cost_centres)

    def get_form_kwargs(self):
        kwargs = super(ChooseCostCentreView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.cost_centre = form.cleaned_data["cost_centre"]
        return super(ChooseCostCentreView, self).form_valid(form)

    def get_success_url(self):
        financial_year = self.get_financial_year()
        return reverse(
            "edit_forecast",
            kwargs={
                "cost_centre_code": self.cost_centre.cost_centre_code,
                "financial_year":financial_year,
            },
        )



class ChooseYearCostCentreView(
    ChooseCostCentreView):

    template_name = "forecast/edit/choose_year_cost_centre.html"
    # form_class = MyCostCentresYearForm

    def get_year_list(self):
        a = FinancialYear.financial_year_objects.future_year_dictionary()
        return FinancialYear.financial_year_objects.future_year_dictionary()

    def get_financial_year(self):
        return get_current_financial_year() + 1
