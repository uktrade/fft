from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.base import TemplateView

from django_tables2 import MultiTableMixin

from core.models import FinancialYear
from core.utils.generic_helpers import get_current_financial_year

from end_of_month.utils import monthly_variance_exists

from forecast.forms import ForecastPeriodForm
from forecast.models import FinancialPeriod
from forecast.utils.access_helpers import (
    can_edit_cost_centre,
    can_forecast_be_edited,
    can_view_forecasts,
)
from forecast.utils.query_fields import (
    ForecastQueryFields,
    SHOW_COSTCENTRE,
    SHOW_DIRECTORATE,
    SHOW_DIT,
    SHOW_GROUP,
)


def get_view_forecast_period_name(period):
    if period < 2000:
        # We are displaying historical forecast
        forecast_period_obj = FinancialPeriod.objects.get(pk=period)
        period_name = forecast_period_obj.period_long_name
    else:
        financial_year_obj = FinancialYear.objects.get(pk=period)
        period_name = financial_year_obj.financial_year_display
    return period_name


class NoCostCentreCodeInURLError(Exception):
    pass


class ForecastViewPermissionMixin(UserPassesTestMixin):
    cost_centre_code = None

    def test_func(self):
        return can_view_forecasts(self.request.user)

    def handle_no_permission(self):
        return redirect(
            reverse(
                "index",
            )
        )


class CostCentrePermissionTest(UserPassesTestMixin):
    cost_centre_code = None
    edit_not_available = False

    def test_func(self):
        if "cost_centre_code" not in self.kwargs:
            raise NoCostCentreCodeInURLError("No cost centre code provided in URL")

        self.cost_centre_code = self.kwargs["cost_centre_code"]

        has_permission = can_edit_cost_centre(
            self.request.user,
            self.cost_centre_code,
        )

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
    # the period can also be a previous archived year
    table_pagination = False

    def __init__(self, *args, **kwargs):
        self._period = None
        self._actual_month_list = None
        self._datamodel = None
        self._table_tag = None
        self._field_infos = None
        self._year = None
        self._show_monthly_variance = None
        self._table_kwargs = None
        self._editable_year = None
        self._show_year_to_date_actuals = None
        super().__init__(*args, **kwargs)

    @property
    def field_infos(self):
        if self._field_infos is None:
            self._field_infos = ForecastQueryFields(self.period)
        return self._field_infos

    @property
    def period(self):
        if self._period is None:
            self._period = self.kwargs["period"]
        return self._period

    @property
    def show_monthly_variance(self):
        if self._show_monthly_variance is None:
            self._show_monthly_variance = monthly_variance_exists(self.period)
        return self._show_monthly_variance

    @property
    def show_year_to_date_actuals(self):
        if self._show_year_to_date_actuals is None:
            # Don't show the year to date spend for future years
            # there is no spending in the future years
            self._show_year_to_date_actuals = self.year <= get_current_financial_year()
        return self._show_year_to_date_actuals

    @property
    def year(self):
        if self._year is None:
            self._year = self.field_infos.selected_year
        return self._year

    @property
    def editable_year(self):
        if self._editable_year is None:
            self._editable_year = self.field_infos.not_archived_year
        return self._editable_year

    @property
    def actual_month_list(self):
        # returns the list of month with actuals in the selected period.
        if self._actual_month_list is None:
            current_year = get_current_financial_year()
            if self.year == 0 or self.year == current_year:
                period = self.period
                if period:
                    # We are displaying previous month forecast
                    self._actual_month_list = (
                        FinancialPeriod.financial_period_info.month_sublist(period)
                    )
                else:
                    self._actual_month_list = (
                        FinancialPeriod.financial_period_info.actual_month_list()
                    )

            elif self.year == get_current_financial_year() - 1:
                # We are displaying the last year before the current one.
                # It is possible that the actuals for march and the adjustments
                # have not been loaded yet, so get the list from
                # the FinancialPeriod
                self._actual_month_list = (
                    FinancialPeriod.
                    financial_period_info.actual_month_previous_year_list()
                )
            elif self.year > current_year:
                # Future forecast
                self._actual_month_list = []
            else:
                # We are displaying historical data, so we need to include
                # the adjustment periods (ADJxx), and everything is actuals
                self._actual_month_list = (
                    FinancialPeriod.financial_period_info.month_adj_display_list()
                )
        return self._actual_month_list

    @property
    def adj_visible_list(self):
        current_year = get_current_financial_year()
        if self.year > current_year:
            list = []
        elif self.year == current_year:
            list = FinancialPeriod.financial_period_info.adj_display_list()
        else:
            # We need to show the Adj periods
            list = FinancialPeriod.financial_period_info.all_adj_list()
        return list

    @property
    def table_kwargs(self):
        if self._table_kwargs is None:
            self._table_kwargs = {
                "actual_month_list": self.actual_month_list,
                "adj_visible_list": self.adj_visible_list,
                "show_monthly_variance": self.show_monthly_variance,
                "show_year_to_date_actuals": self.show_year_to_date_actuals,
            }
        return self._table_kwargs

    @property
    def data_model(self):
        return self.field_infos.datamodel

    @property
    def table_tag(self):
        if self._table_tag is None:
            current_year = get_current_financial_year()
            if self.year > current_year:
                self._table_tag = (
                    f"Future forecast for {get_view_forecast_period_name(self.year)}"
                )
            else:
                period = self.period
                if period:
                    self._table_tag = (
                        f"Historical data for {get_view_forecast_period_name(period)}"
                    )
                else:
                    self._table_tag = ""
        return self._table_tag


class PeriodView(TemplateView):
    table_pagination = False

    def period_form(self):
        return ForecastPeriodForm(selected_period=self.period)


class CostCentreForecastMixin(PeriodView):
    hierarchy_type = SHOW_COSTCENTRE

    @property
    def cost_centre_code(self):
        return self.kwargs["cost_centre_code"]

    @property
    def costcentre_code(self):
        return self.kwargs["cost_centre_code"]

    def cost_centre(self):
        return self.field_infos.cost_centre(
            cost_centre_code=self.costcentre_code,
        )

    @property
    def cost_centre_name(self):
        return self.cost_centre().cost_centre_name

    @property
    def directorate_code(self):
        if self.field_infos.not_archived_year:
            return self.cost_centre().directorate.directorate_code
        else:
            return self.cost_centre().directorate_code

    @property
    def directorate_name(self):
        if self.field_infos.not_archived_year:
            return self.cost_centre().directorate.directorate_name
        else:
            return self.cost_centre().directorate_name

    @property
    def group_code(self):
        if self.field_infos.not_archived_year:
            return self.cost_centre().directorate.group.group_code
        else:
            return self.cost_centre().group_code

    @property
    def group_name(self):
        if self.field_infos.not_archived_year:
            return self.cost_centre().directorate.group.group_name
        else:
            return self.cost_centre().group_name


class DirectorateForecastMixin(PeriodView):
    hierarchy_type = SHOW_DIRECTORATE

    @property
    def directorate_code(self):
        return self.kwargs["directorate_code"]

    def directorate(self):
        return self.field_infos.directorate(self.directorate_code)

    @property
    def directorate_name(self):
        return self.directorate().directorate_name

    @property
    def group_code(self):
        if self.field_infos.not_archived_year:
            return self.directorate().group.group_code
        else:
            return self.directorate().group_code

    @property
    def group_name(self):
        if self.field_infos.not_archived_year:
            return self.directorate().group.group_name
        else:
            return self.directorate().group_name


class GroupForecastMixin(PeriodView):
    hierarchy_type = SHOW_GROUP

    def group(self):
        return self.field_infos.group(self.group_code)

    @property
    def group_code(self):
        return self.kwargs["group_code"]

    @property
    def group_name(self):
        return self.group().group_name


class DITForecastMixin(PeriodView):
    hierarchy_type = SHOW_DIT
