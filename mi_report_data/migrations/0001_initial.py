# Generated by Django 3.2.13 on 2022-08-18 15:55

from django.db import migrations


"""
The following views unpivot the views used for each archived months,
and create the format required for the creations of the MI reports on Data Workspace.
Even if this is not the most efficient way to do it 
(because the queries are based on other queries),
it has the big advantage of starting from the same  queries used for displaying 
and downloading data from FFT.
It would be more efficient to start from the original tables,
but we would end up with two different ways of extracting similar data.
Any discrepancy would be a nightmare to fix!
"""


drop_view_sql = """
        DROP VIEW IF EXISTS mi_report_monthly_forecast_apr; 
        DROP VIEW IF EXISTS mi_report_monthly_forecast_may; 
        DROP VIEW IF EXISTS mi_report_monthly_forecast_jun; 
        DROP VIEW IF EXISTS mi_report_monthly_forecast_jul; 
        DROP VIEW IF EXISTS mi_report_monthly_forecast_aug; 
        DROP VIEW IF EXISTS mi_report_monthly_forecast_sep; 
        DROP VIEW IF EXISTS mi_report_monthly_forecast_oct; 
        DROP VIEW IF EXISTS mi_report_monthly_forecast_nov; 
        DROP VIEW IF EXISTS mi_report_monthly_forecast_dec; 
        DROP VIEW IF EXISTS mi_report_monthly_forecast_jan; 
        DROP VIEW IF EXISTS mi_report_monthly_forecast_feb; 
        DROP VIEW IF EXISTS mi_report_monthly_forecast_mar; 
        DROP VIEW IF EXISTS mi_report_monthly_forecast_adj1; 
        DROP VIEW IF EXISTS mi_report_monthly_forecast_adj2; 
        DROP VIEW IF EXISTS mi_report_monthly_forecast_adj3; 
        DROP VIEW IF EXISTS mi_report_current_actual; 
        DROP VIEW IF EXISTS mi_report_current_forecast;
        DROP VIEW IF EXISTS mi_report_current_period;
        DROP VIEW IF EXISTS mi_report_archived_budget_view;
        DROP VIEW IF EXISTS mi_report_current_budget_view;
"""

create_view_sql = """
CREATE VIEW mi_report_monthly_forecast_apr as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) as actual,
    unnest( array[0, "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "jan", "feb", "mar", "adj1", "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_apr 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE VIEW mi_report_monthly_forecast_may as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) as actual,
    unnest( array[0, 0, "jun", "jul", "aug", "sep", "oct", "nov", "dec", "jan", "feb", "mar", "adj1", "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_may 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE VIEW mi_report_monthly_forecast_jun as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) as actual,
    unnest( array[0, 0, 0, "jul", "aug", "sep", "oct", "nov", "dec", "jan", "feb", "mar", "adj1", "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_jun 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE VIEW mi_report_monthly_forecast_jul as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", "jul", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) as actual,
    unnest( array[0, 0, 0, 0, "aug", "sep", "oct", "nov", "dec", "jan", "feb", "mar", "adj1", "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_jul 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE VIEW mi_report_monthly_forecast_aug as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", "jul", "aug", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) as actual,
    unnest( array[0, 0, 0, 0, 0, "sep", "oct", "nov", "dec", "jan", "feb", "mar", "adj1", "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_aug 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE VIEW mi_report_monthly_forecast_sep as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", "jul", "aug", "sep", 0, 0, 0, 0, 0, 0, 0, 0, 0]) as actual,
    unnest( array[0, 0, 0, 0, 0, 0, "oct", "nov", "dec", "jan", "feb", "mar", "adj1", "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_sep 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE VIEW mi_report_monthly_forecast_oct as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", "jul", "aug", "sep", "oct", 0, 0, 0, 0, 0, 0, 0, 0]) as actual,
    unnest( array[0, 0, 0, 0, 0, 0, 0, "nov", "dec", "jan", "feb", "mar", "adj1", "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_oct 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE VIEW mi_report_monthly_forecast_nov as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", 0, 0, 0, 0, 0, 0, 0]) as actual,
    unnest( array[0, 0, 0, 0, 0, 0, 0, 0, "dec", "jan", "feb", "mar", "adj1", "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_nov 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE VIEW mi_report_monthly_forecast_dec as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", 0, 0, 0, 0, 0, 0]) as actual,
    unnest( array[0, 0, 0, 0, 0, 0, 0, 0, 0, "jan", "feb", "mar", "adj1", "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_dec 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE VIEW mi_report_monthly_forecast_jan as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "jan", 0, 0, 0, 0, 0]) as actual,
    unnest( array[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "feb", "mar", "adj1", "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_jan 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE VIEW mi_report_monthly_forecast_feb as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "jan", "feb", 0, 0, 0, 0]) as actual,
    unnest( array[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "mar", "adj1", "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_feb 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE VIEW mi_report_monthly_forecast_mar as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "jan", "feb", "mar", 0, 0, 0]) as actual,
    unnest( array[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "adj1", "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_mar 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE VIEW mi_report_monthly_forecast_adj1 as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "jan", "feb", "mar", "adj1", 0, 0]) as actual,
    unnest( array[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_adj1 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE VIEW mi_report_monthly_forecast_adj2 as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "jan", "feb", "mar", "adj1", "adj2", 0]) as actual,
    unnest( array[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "adj3"]) as forecast
    FROM public.monthly_forecast_adj2 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE VIEW mi_report_monthly_forecast_adj3 as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "jan", "feb", "mar", "adj1", "adj2", "adj3"]) as actual,
    unnest( array[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) as forecast
    FROM public.monthly_forecast_adj3 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE VIEW mi_report_current_period as
SELECT 
    financial_code_id,
    financial_year_id,
    unnest(ARRAY[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]) AS financial_period_id,
    unnest(ARRAY[apr, may, jun, jul, aug, sep, oct, nov, "dec", jan, feb, mar, adj1, adj2, adj3
				 ]) AS amount
   FROM annual_forecast 
  WHERE (annual_forecast.financial_year_id IN ( SELECT core_financialyear.financial_year
           FROM core_financialyear
          WHERE core_financialyear.current = true));


CREATE VIEW mi_report_current_actual AS
  SELECT financial_code_id,
    financial_year_id,
    financial_period_id,
    0 AS forecast, ar.archived_period_id,
    coalesce(amount,0) AS actual
   FROM mi_report_current_period, (SELECT min(archived_period_id) as archived_period_id
	FROM end_of_month_endofmonthstatus where archived = false) ar
  WHERE  financial_period_id IN  
  (SELECT financial_period_code FROM forecast_financialperiod WHERE actual_loaded = true);

CREATE VIEW mi_report_current_forecast
 AS
 SELECT financial_code_id,
    financial_year_id,
    financial_period_id,
    coalesce(amount,0)  AS forecast, ar.archived_period_id,
    0 AS actual
   FROM mi_report_current_period, (SELECT min(archived_period_id) as archived_period_id
	FROM end_of_month_endofmonthstatus where archived = false) ar
  WHERE  financial_period_id IN  
  (SELECT financial_period_code FROM forecast_financialperiod WHERE actual_loaded = false);


CREATE VIEW mi_report_current_budget_view
AS
 SELECT financial_code_id,
    amount AS budget,
    financial_period_id,
    financial_year_id,
    ar.archived_period_id
   FROM forecast_budgetmonthlyfigure, (SELECT min(archived_period_id) as archived_period_id
	FROM end_of_month_endofmonthstatus where archived = false) ar
  WHERE financial_year_id IN ( SELECT financial_year
           FROM core_financialyear
          WHERE core_financialyear.current = true)
		  AND archived_status_id IS NULL;

CREATE VIEW mi_report_archived_budget_view
 AS
 SELECT f.financial_code_id,
    f.amount AS budget,
    f.financial_period_id,
    f.financial_year_id,
    fp.archived_period_id
   FROM forecast_budgetmonthlyfigure f
     CROSS JOIN end_of_month_endofmonthstatus fp
  WHERE (f.financial_year_id IN ( SELECT core_financialyear.financial_year
           FROM core_financialyear
          WHERE core_financialyear.current = true)) AND f.archived_status_id IS NULL AND (f.financial_period_id IN ( SELECT forecast_financialperiod.financial_period_code
           FROM forecast_financialperiod
          WHERE forecast_financialperiod.actual_loaded = true)) AND fp.archived_period_id >= f.financial_period_id
UNION
 SELECT forecast_budgetmonthlyfigure.financial_code_id,
    forecast_budgetmonthlyfigure.amount AS budget,
    forecast_budgetmonthlyfigure.financial_period_id,
    forecast_budgetmonthlyfigure.financial_year_id,
    forecast_budgetmonthlyfigure.archived_status_id AS archived_period_id
   FROM forecast_budgetmonthlyfigure
  WHERE (forecast_budgetmonthlyfigure.financial_year_id IN ( SELECT core_financialyear.financial_year
           FROM core_financialyear
          WHERE core_financialyear.current = true)) AND forecast_budgetmonthlyfigure.archived_status_id IS NOT NULL;


"""


class Migration(migrations.Migration):

    dependencies = [
        ("previous_years", "0004_auto_20210707_1008"),
    ]
    # Use a materialized view for the following because it will not change.
    operations = [
        migrations.RunSQL(f"{drop_view_sql} {create_view_sql}", drop_view_sql),
        migrations.RunSQL(
            """
                DROP materialized VIEW if exists  mi_report_periods;
         CREATE materialized VIEW mi_report_periods
                 AS
                 SELECT f.financial_period_code AS financial_period_id,
                    a.financial_period_code AS archived_period_id
                   FROM forecast_financialperiod f
                     CROSS JOIN forecast_financialperiod a;

        """,
            """
                DROP VIEW if exists mi_report_periods;
                """,
        ),
        migrations.RunSQL(
            """
            DROP VIEW if exists mi_report_empty_data;            
            CREATE VIEW mi_report_empty_data as
                  SELECT financial_code_id,
                    0 AS budget,
                    0 AS forecast,
                    0 AS actual,
                    financial_period_id,
                    financial_year_id,
                    archived_period_id
                   FROM (
                    SELECT DISTINCT forecast_budgetmonthlyfigure.financial_code_id,
                    forecast_budgetmonthlyfigure.financial_year_id
                   FROM forecast_budgetmonthlyfigure
                        UNION
                 SELECT DISTINCT forecast_forecastmonthlyfigure.financial_code_id,
                    forecast_forecastmonthlyfigure.financial_year_id
                   FROM forecast_forecastmonthlyfigure
                ) a
                     CROSS JOIN mi_report_periods;

        """,
            """
                DROP VIEW if exists mi_report_empty_data;
                """,
        ),
    ]
