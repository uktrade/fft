import json

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views.generic.edit import FormView

from core.models import FinancialYear
from core.utils.generic_helpers import get_current_financial_year, get_year_display
from costcentre.forms import MyCostCentresForm
from forecast.utils.access_helpers import (
    can_edit_at_least_one_cost_centre,
    can_forecast_be_edited,
    can_future_forecast_be_edited,
    get_user_cost_centres,
)


class ChooseCostCentreView(
    UserPassesTestMixin,
    FormView,
):
    template_name = "forecast/edit/choose_cost_centre.html"
    form_class = MyCostCentresForm
    cost_centre = None
    next_page = "forecast"

    def test_func(self):
        can_edit = can_edit_at_least_one_cost_centre(self.request.user)

        if not can_edit:
            raise PermissionDenied()

        self.future_can_be_edited = can_future_forecast_be_edited(self.request.user)
        self.current_year_can_be_edited = can_forecast_be_edited(self.request.user)
        return True

    def get_financial_year(self):
        current_financial_year = get_current_financial_year()
        if self.current_year_can_be_edited:
            return current_financial_year
        else:
            # Theoretically, I should check that the next year exists.
            # But if it does not exist, it will be created later on
            return current_financial_year + 1

    def get_financial_year_display(self):
        if self.current_year_can_be_edited:
            return "current"
        return get_year_display(get_current_financial_year() + 1)

    def get_financial_years(self):
        financial_years = []
        if self.future_can_be_edited:
            if self.current_year_can_be_edited:
                financial_years.append(
                    {
                        "financial_year": get_current_financial_year(),
                        "financial_year_display": "Current",
                    }
                )

            for year in FinancialYear.financial_year_objects.future_year_dictionary():
                financial_years.append(year)

        return json.dumps(financial_years)

    def get_user_cost_centres(self):
        user_cost_centres = get_user_cost_centres(
            self.request.user,
        )

        cost_centres = []
        for cost_centre in user_cost_centres:
            cost_centres.append(
                {
                    "name": cost_centre.cost_centre_name,
                    "code": cost_centre.cost_centre_code,
                }
            )

        return json.dumps(cost_centres)

    def get_page_header(self):
        return self.next_page.capitalize()

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
                "financial_year": financial_year,
            },
        )
