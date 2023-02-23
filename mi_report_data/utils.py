from django.db import connection


def refresh_materialised_views():
    # Brute force: execute an sql query refreshing all the materialized views
    # used to get the archived data in the correct format for the data workspace
    sql_refresh = """
        REFRESH MATERIALIZED VIEW mi_report_monthly_forecast_apr;
        REFRESH MATERIALIZED VIEW mi_report_monthly_forecast_may;
        REFRESH MATERIALIZED VIEW mi_report_monthly_forecast_jun;
        REFRESH MATERIALIZED VIEW mi_report_monthly_forecast_jul;
        REFRESH MATERIALIZED VIEW mi_report_monthly_forecast_aug;
        REFRESH MATERIALIZED VIEW mi_report_monthly_forecast_sep;
        REFRESH MATERIALIZED VIEW mi_report_monthly_forecast_oct;
        REFRESH MATERIALIZED VIEW mi_report_monthly_forecast_nov;
        REFRESH MATERIALIZED VIEW mi_report_monthly_forecast_dec;
        REFRESH MATERIALIZED VIEW mi_report_monthly_forecast_jan;
        REFRESH MATERIALIZED VIEW mi_report_monthly_forecast_feb;
        REFRESH MATERIALIZED VIEW mi_report_monthly_forecast_mar;
        REFRESH MATERIALIZED VIEW mi_report_monthly_forecast_adj1;
        REFRESH MATERIALIZED VIEW mi_report_monthly_forecast_adj2;
        REFRESH MATERIALIZED VIEW mi_report_monthly_forecast_adj3;
    """
    with connection.cursor() as cursor:
        cursor.execute(sql_refresh)
