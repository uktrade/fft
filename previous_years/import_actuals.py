import logging

from django.core.cache import cache
from django.db import connection

from previous_years.models import (
    ArchivedActualUploadMonthlyFigure,
    ArchivedForecastData,
)

logger = logging.getLogger(__name__)


def copy_previous_year_actuals_to_monthly_figure(period_obj, financial_year):
    # Now copy the newly uploaded actuals to the previous year figure table
    # hack alert: the name of the fields in the model are identical to the short name
    # of the period, but in lowercase
    # Use direct sql for speed.
    period_name = period_obj.period_short_name.lower()

    ArchivedForecastData.objects.filter(financial_year=financial_year).update(
        **{period_name: 0}
    )

    sql_update = (
        f"UPDATE previous_years_archivedforecastdata t "
        f"SET  updated=now(), {period_name}=u.amount	"
        f"FROM previous_years_archivedactualuploadmonthlyfigure u "
        f"WHERE  "
        f"t.financial_code_id = u.financial_code_id and "
        f"t.financial_year_id = u.financial_year_id and "
        f"t.financial_year_id = {financial_year};"
    )

    sql_insert = (
        f"INSERT INTO previous_years_archivedforecastdata "
        f"(created, updated, archived,"
        f"budget,"
        f'apr, may, jun, jul, aug, sep, oct, nov, "dec", jan, feb, mar, '
        f'adj1, adj2, adj3,'
        f"financial_code_id, financial_year_id)"
        f"SELECT now(), now(), now(), "
        f"0, "
        f"0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "
        f"financial_code_id, financial_year_id "
        f"FROM previous_years_archivedactualuploadmonthlyfigure "
        f"WHERE "
        f"financial_year_id = {financial_year}  and "
        f" financial_code_id "
        f"not in (select financial_code_id "
        f"from previous_years_archivedforecastdata where "
        f"financial_year_id = {financial_year});"
    )

    with connection.cursor() as cursor:
        cursor.execute(sql_insert)
        cursor.execute(sql_update)

    ArchivedActualUploadMonthlyFigure.objects.filter(
        financial_year=financial_year
    ).delete()
    # clear the caches, used to store the forecast data for performance reason
    # otherwise the new data will not appear on the view forecast page until
    # the cache expires, up to a week!
    cache.clear()
