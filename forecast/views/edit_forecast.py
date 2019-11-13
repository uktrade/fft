import json

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import (
    render,
)
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from guardian.shortcuts import get_objects_for_user

from costcentre.forms import (
    MyCostCentresForm,
)
from costcentre.models import CostCentre

from forecast.forms import (
    AddForecastRowForm,
    EditForm,
)
from forecast.models import (
    FinancialPeriod,
    MonthlyFigure,
)
from forecast.tables import (
    ForecastTable,
)
from forecast.views.base import (
    ForecastPermissionTest,
    NoCostCentreCodeInURLError,
)

TEST_COST_CENTRE = 888812
TEST_FINANCIAL_YEAR = 2019


class ChooseCostCentreView(UserPassesTestMixin, FormView):
    template_name = "forecast/edit/choose_cost_centre.html"
    form_class = MyCostCentresForm
    cost_centre = None

    def test_func(self):
        cost_centres = get_objects_for_user(
            self.request.user,
            "costcentre.change_costcentre",
        )

        # If user has permission on
        # one or more CCs then let them view
        return cost_centres.count() > 0

    def get_form_kwargs(self):
        kwargs = super(ChooseCostCentreView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.cost_centre = form.cleaned_data['cost_centre']
        return super(ChooseCostCentreView, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            "edit_forecast",
            kwargs={
                'cost_centre_code': self.cost_centre.cost_centre_code
            }
        )


class AddRowView(ForecastPermissionTest, FormView):
    template_name = "forecast/edit/add.html"
    form_class = AddForecastRowForm
    financial_year_id = TEST_FINANCIAL_YEAR
    cost_centre_code = None

    def get_cost_centre(self):
        if self.cost_centre_code is not None:
            return

        if 'cost_centre_code' not in self.kwargs:
            raise NoCostCentreCodeInURLError(
                "No cost centre code provided in URL"
            )

        self.cost_centre_code = self.kwargs["cost_centre_code"]

    def get_success_url(self):
        self.get_cost_centre()

        return reverse(
            "edit_forecast",
            kwargs={
                'cost_centre_code': self.cost_centre_code
            }
        )

    def cost_centre_details(self):
        self.get_cost_centre()

        cost_centre = CostCentre.objects.get(
            cost_centre_code=self.cost_centre_code,
        )
        return {
            "group": cost_centre.directorate.group.group_name,
            "directorate": cost_centre.directorate.directorate_name,
            "cost_centre_name": cost_centre.cost_centre_name,
            "cost_centre_num": cost_centre.cost_centre_code,
        }

    def form_valid(self, form):
        self.get_cost_centre()
        data = form.cleaned_data
        for financial_period in range(1, 13):
            monthly_figure = MonthlyFigure(
                financial_year_id=self.financial_year_id,
                financial_period_id=financial_period,
                cost_centre_id=self.cost_centre_code,
                programme=data["programme"],
                natural_account_code=data["natural_account_code"],
                analysis1_code=data["analysis1_code"],
                analysis2_code=data["analysis2_code"],
                project_code=data["project_code"],
                amount=0,
            )
            monthly_figure.save()

        return super().form_valid(form)


class EditForecastView(ForecastPermissionTest, TemplateView):
    template_name = "forecast/edit/edit.html"

    def cost_centre_details(self):
        return {
            "group": "Test group",
            "directorate": "Test directorate",
            "cost_centre_name": "Test cost centre name",
            "cost_centre_num": self.cost_centre_code,
        }

    def table(self):
        field_dict = {
            "cost_centre__directorate": "Directorate",
            "cost_centre__directorate__directorate_name": "Name",
            "natural_account_code": "NAC",
            "cost_centre": self.cost_centre_code,
        }

        q1 = MonthlyFigure.pivot.pivot_data(
            field_dict.keys(), {"cost_centre": self.cost_centre_code}
        )

        return ForecastTable(field_dict, q1)


def edit_forecast_prototype(request):
    financial_year = TEST_FINANCIAL_YEAR
    cost_centre_code = TEST_COST_CENTRE

    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            cost_centre_code = form.cleaned_data["cost_centre_code"]
            financial_year = form.cleaned_data["financial_year"]

            cell_data = json.loads(form.cleaned_data["cell_data"])

            for key, cell in cell_data.items():
                if cell["editable"]:
                    monthly_figure = MonthlyFigure.objects.filter(
                        cost_centre__cost_centre_code=cost_centre_code,
                        financial_year__financial_year=financial_year,
                        financial_period__period_short_name__iexact=cell["key"],
                        programme__programme_code=cell["programmeCode"],
                        natural_account_code__natural_account_code=cell[
                            "naturalAccountCode"
                        ],
                    ).first()
                    monthly_figure.amount = int(float(cell["value"]))
                    monthly_figure.save()
    else:
        form = EditForm(
            initial={
                "financial_year": financial_year,
                "cost_centre_code": cost_centre_code,
            }
        )
    pivot_filter = {"cost_centre__cost_centre_code": "{}".format(cost_centre_code)}
    monthly_figures = MonthlyFigure.pivot.pivot_data({}, pivot_filter)

    # TODO - Luisella to restrict to financial year
    editable_periods = list(FinancialPeriod.objects.filter(actual_loaded=False).all())

    editable_periods_dump = serializers.serialize("json", editable_periods)

    forecast_dump = json.dumps(list(monthly_figures), cls=DjangoJSONEncoder)

    return render(
        request,
        "forecast/edit/edit_prototype.html",
        {
            "form": form,
            "editable_periods_dump": editable_periods_dump,
            "forecast_dump": forecast_dump,
        },
    )
