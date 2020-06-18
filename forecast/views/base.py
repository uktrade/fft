from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from django_tables2 import MultiTableMixin

from end_of_month.models import forecast_budget_view_model

from forecast.forms import ForecastPeriodForm
from forecast.models import FinancialPeriod
from forecast.utils.access_helpers import (
    can_edit_cost_centre,
    can_forecast_be_edited,
    can_view_forecasts,
)


class NoCostCentreCodeInURLError(Exception):
    pass


class ForecastViewPermissionMixin(UserPassesTestMixin):
    cost_centre_code = None

    def test_func(self):
        return can_view_forecasts(self.request.user)

    def handle_no_permission(self):
        return redirect(reverse("index",))


class CostCentrePermissionTest(UserPassesTestMixin):
    cost_centre_code = None
    edit_not_available = False

    def test_func(self):
        if "cost_centre_code" not in self.kwargs:
            raise NoCostCentreCodeInURLError("No cost centre code provided in URL")

        self.cost_centre_code = self.kwargs["cost_centre_code"]

        has_permission = can_edit_cost_centre(self.request.user, self.cost_centre_code,)

        user_can_edit = can_forecast_be_edited(self.request.user)

        if not user_can_edit:
            self.edit_not_available = True
            return False

        return has_permission

    def handle_no_permission(self):
        if self.edit_not_available:
            return redirect(reverse("edit_unavailable"))
        else:
            return redirect(
                reverse(
                    "forecast_cost_centre",
                    kwargs={
                        "cost_centre_code": self.cost_centre_code,
                        "period": 0,
                    },
                )
            )


class ForecastViewTableMixin(MultiTableMixin):
    # It handles the differences caused by viewing
    # forecasts entered in different period.
    def __init__(self, *args, **kwargs):
        self._period = None
        self._month_list = None
        self._datamodel = None
        self._table_tag = None

        super().__init__(*args, **kwargs)

    @property
    def period(self):
        if self._period is None:
            self._period = self.kwargs["period"]
        return self._period

    @property
    def month_list(self):
        if self._month_list is None:
            period = self.period
            if period:
                # We are displaying historical forecast
                self._month_list = FinancialPeriod.financial_period_info.month_sublist(
                    period - 1
                )
            else:
                self._month_list = (
                    FinancialPeriod.financial_period_info.actual_month_list()
                )
        return self._month_list

    @property
    def data_model(self):
        if self._datamodel is None:
            self._datamodel = forecast_budget_view_model[self.period]
        return self._datamodel

    @property
    def table_tag(self):
        if self._table_tag is None:
            period = self.period
            if period:
                # We are displaying historical forecast
                forecast_period_obj = FinancialPeriod.objects.get(pk=period)
                self._table_tag = (
                    f"Historical data for {forecast_period_obj.period_long_name}"
                )
            else:
                self._table_tag = ""
        return self._table_tag


class PeriodFormView(FormView):
    form_class = ForecastPeriodForm

    # https://gist.github.com/vero4karu/ec0f82bb3d302961503d
    def get_form_kwargs(self):
        kwargs = super(PeriodFormView, self).get_form_kwargs()
        kwargs.update({"selected_period": self.period})
        return kwargs


class PeriodView(TemplateView):
    def period_form(self):
        return ForecastPeriodForm(selected_period=self.period)
