# Generated by Django 3.2.16 on 2023-02-23 15:33

from django.db import migrations

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
"""

create_view_sql = """
CREATE MATERIALIZED VIEW mi_report_monthly_forecast_apr as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) as actual,
    unnest( array[0, "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "jan", "feb", "mar", "adj1", "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_apr 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE MATERIALIZED VIEW mi_report_monthly_forecast_may as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) as actual,
    unnest( array[0, 0, "jun", "jul", "aug", "sep", "oct", "nov", "dec", "jan", "feb", "mar", "adj1", "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_may 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE MATERIALIZED VIEW mi_report_monthly_forecast_jun as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) as actual,
    unnest( array[0, 0, 0, "jul", "aug", "sep", "oct", "nov", "dec", "jan", "feb", "mar", "adj1", "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_jun 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE MATERIALIZED VIEW mi_report_monthly_forecast_jul as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", "jul", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) as actual,
    unnest( array[0, 0, 0, 0, "aug", "sep", "oct", "nov", "dec", "jan", "feb", "mar", "adj1", "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_jul 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE MATERIALIZED VIEW mi_report_monthly_forecast_aug as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", "jul", "aug", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) as actual,
    unnest( array[0, 0, 0, 0, 0, "sep", "oct", "nov", "dec", "jan", "feb", "mar", "adj1", "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_aug 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE MATERIALIZED VIEW mi_report_monthly_forecast_sep as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", "jul", "aug", "sep", 0, 0, 0, 0, 0, 0, 0, 0, 0]) as actual,
    unnest( array[0, 0, 0, 0, 0, 0, "oct", "nov", "dec", "jan", "feb", "mar", "adj1", "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_sep 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE MATERIALIZED VIEW mi_report_monthly_forecast_oct as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", "jul", "aug", "sep", "oct", 0, 0, 0, 0, 0, 0, 0, 0]) as actual,
    unnest( array[0, 0, 0, 0, 0, 0, 0, "nov", "dec", "jan", "feb", "mar", "adj1", "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_oct 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE MATERIALIZED VIEW mi_report_monthly_forecast_nov as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", 0, 0, 0, 0, 0, 0, 0]) as actual,
    unnest( array[0, 0, 0, 0, 0, 0, 0, 0, "dec", "jan", "feb", "mar", "adj1", "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_nov 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE MATERIALIZED VIEW mi_report_monthly_forecast_dec as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", 0, 0, 0, 0, 0, 0]) as actual,
    unnest( array[0, 0, 0, 0, 0, 0, 0, 0, 0, "jan", "feb", "mar", "adj1", "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_dec 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE MATERIALIZED VIEW mi_report_monthly_forecast_jan as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "jan", 0, 0, 0, 0, 0]) as actual,
    unnest( array[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "feb", "mar", "adj1", "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_jan 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE MATERIALIZED VIEW mi_report_monthly_forecast_feb as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "jan", "feb", 0, 0, 0, 0]) as actual,
    unnest( array[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "mar", "adj1", "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_feb 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE MATERIALIZED VIEW mi_report_monthly_forecast_mar as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "jan", "feb", "mar", 0, 0, 0]) as actual,
    unnest( array[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "adj1", "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_mar 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE MATERIALIZED VIEW mi_report_monthly_forecast_adj1 as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "jan", "feb", "mar", "adj1", 0, 0]) as actual,
    unnest( array[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "adj2", "adj3"]) as forecast
    FROM public.monthly_forecast_adj1 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE MATERIALIZED VIEW mi_report_monthly_forecast_adj2 as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "jan", "feb", "mar", "adj1", "adj2", 0]) as actual,
    unnest( array[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "adj3"]) as forecast
    FROM public.monthly_forecast_adj2 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);

CREATE MATERIALIZED VIEW mi_report_monthly_forecast_adj3 as 
    SELECT archived_period_id, financial_code_id, financial_year_id,
    unnest( array[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]) AS financial_period_id,
    unnest( array["apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "jan", "feb", "mar", "adj1", "adj2", "adj3"]) as actual,
    unnest( array[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) as forecast
    FROM public.monthly_forecast_adj3 
    WHERE financial_year_id IN
    (SELECT financial_year FROM public.core_financialyear where current = true);
"""

class Migration(migrations.Migration):

    dependencies = [
        ('mi_report_data', '0008_period_0_model'),
    ]

    operations = [
        migrations.RunSQL(f"{drop_view_sql} {create_view_sql}", drop_view_sql),
    ]