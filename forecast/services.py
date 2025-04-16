from typing import Iterable

from guardian.shortcuts import get_objects_for_user, remove_perm

from core.constants import PERIODS
from core.models import FinancialYear
from costcentre.models import CostCentre
from forecast.models import FinancialCode, FinancialPeriod, ForecastMonthlyFigure
from forecast.permission_shortcuts import assign_perm


class FinancialCodeForecastService:
    def __init__(
        self,
        *,
        financial_code: FinancialCode,
        year: FinancialYear,
        override_locked: bool = False,
    ):
        self.financial_code = financial_code
        self.year = year
        self.override_locked = override_locked

        if not FinancialYear.objects.forecast().contains(self.year):
            raise ValueError("self.year must be a forecast financial year")

    def update_period(self, *, period: int | FinancialPeriod, amount: int):
        if isinstance(period, int):
            period = FinancialPeriod.objects.get(pk=period)

        assert isinstance(period, FinancialPeriod)

        # actuals only apply to past and current years and not to future years.
        if self.year.current and period.actual_loaded:
            return

        if self.financial_code.is_locked and not self.override_locked:
            return

        figure, _ = ForecastMonthlyFigure.objects.get_or_create(
            financial_code=self.financial_code,
            financial_year=self.year,
            financial_period=period,
            archived_status=None,
        )

        # NOTE: Not deleting the figure if the amount is 0 like in other places.

        figure.amount = amount
        figure.save()

    def update(self, forecast: list[int]):
        assert len(forecast) == len(PERIODS)

        for period in PERIODS:
            self.update_period(period=period, amount=forecast[period - 1])


def get_users_cost_centres(user):
    return get_objects_for_user(
        user,
        "costcentre.change_costcentre",
        with_superuser=False,
        accept_global_perms=False,
    )


def update_users_cost_centres(user, cost_centres: Iterable[CostCentre]):
    current_cost_centres = get_users_cost_centres(user)

    for cost_centre in cost_centres:
        if cost_centre in current_cost_centres:
            continue

        assign_perm("costcentre.change_costcentre", user, cost_centre)

    for cost_centre in current_cost_centres:
        if cost_centre in cost_centres:
            continue

        remove_perm("costcentre.change_costcentre", user, cost_centre)
