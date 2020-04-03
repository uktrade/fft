from django.db import (
    DatabaseError,
    transaction,
)
from django.db.models import F, Value, IntegerField

from end_of_month.models import EndOfMonthStatus

from forecast.models import (BudgetMonthlyFigure,
                             FinancialPeriod,
                             ForecastMonthlyFigure,
                             )

from simple_history.utils import bulk_create_with_history

@transaction.atomic
def end_of_month_archive(end_of_month_info):
    try:
        with transaction.atomic():
            period_id = end_of_month_info.archived_period.financial_period_code
            # Use transaction
            # Add archive period to all the active forecast
            archived_periods = ForecastMonthlyFigure.objects.filter(
                financial_period__financial_period_code__gt=period_id,
                archived_status__isnull=True)
            archived_periods.update(archived_status=end_of_month_info)

            # Copy forecast just archived to current forecast
            # current_forecast = ForecastMonthlyFigure.objects.filter(archived_status=end_of_month_info)\
            #     .values('financial_year',
            #             'financial_period',
            #             'financial_code',
            #             'amount',
            # ).annotate(starting_amount=F('amount'),
            #            archived_status=Value(None, output_field=IntegerField()))

            current_forecast = ForecastMonthlyFigure.objects.filter(archived_status=end_of_month_info)\
                .values('financial_year',
                        'financial_period',
                        'financial_code',
                        'amount',
            ).annotate(starting_amount=F('amount'), pk = 100000+F'pk')

            # models.TestModel.objects.bulk_create(instances)
            objs = bulk_create_with_history(current_forecast, ForecastMonthlyFigure, batch_size=500)
            # Refresh the amount to  the start of month field

            # Archive the budget
            # set the archived status to archived
    except DatabaseError:
        obj.active = False
