from core.constants import PERIODS
from core.models import FinancialYear
from forecast.models import FinancialCode, FinancialPeriod, ForecastMonthlyFigure


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

    def update_period(self, *, period: int | FinancialPeriod, amount: int):
        if isinstance(period, int):
            period = FinancialPeriod.objects.get(pk=period)

        assert isinstance(period, FinancialPeriod)

        if period.actual_loaded:
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
