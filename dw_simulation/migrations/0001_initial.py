# Generated by Django 3.2.13 on 2022-08-19 13:35

from django.db import migrations

# Create in FFT tables that will be created in data lake by the pipelines
# Needed for testing before creating the pipelines
drop_sql = """
DROP VIEW IF EXISTS dw_current_year_data;

DROP VIEW IF EXISTS dw_actual_forecast_ytd;
DROP VIEW IF EXISTS dw_actual_ytd;
DROP VIEW IF EXISTS dw_current_rates;
DROP VIEW IF EXISTS dw_current_year_outturn;
DROP VIEW IF EXISTS dw_previous_period_forecast;

DROP TABLE IF EXISTS public.dw_simulation_mi_report_forecast_actual;
DROP TABLE IF EXISTS public.dw_simulation_mi_report_budget;
DROP TABLE IF EXISTS dw_simulation_mi_report_previous_year_actual;
DROP TABLE IF EXISTS dw_simulation_financial_period_in_use;
DROP TABLE IF EXISTS dw_simulation_financial_period;

"""

create_sql = """
CREATE TABLE IF NOT EXISTS dw_simulation_financial_period
(
    financial_period_code integer,
    period_short_name character varying(10)
);

CREATE TABLE IF NOT EXISTS  dw_simulation_mi_report_forecast_actual
(
    cost_centre_code character varying(6),
    actual_nac integer,
    programme_code character varying(50),
    contract_code character varying,
    market_code character varying,
    project_code character varying,
    expenditure_type character varying(100),
    expenditure_type_description character varying(100),
    financial_code integer,
    actual numeric,
    forecast numeric,
    actual_loaded boolean, 
    financial_period_code integer,
    financial_period_name character varying(10),
    archived_financial_period_code integer,
    archived_financial_period_name character varying(10),
    financial_year integer,
    archiving_year integer
);

CREATE TABLE IF NOT EXISTS public.dw_simulation_mi_report_budget
(
    cost_centre_code character varying(6),
    actual_nac integer,
    programme_code character varying(50),
    contract_code character varying,
    market_code character varying,
    project_code character varying,
    expenditure_type character varying(100),
    expenditure_type_description character varying(100),
    financial_code integer,
    budget numeric,
    financial_period_code integer,
    financial_period_name character varying(10),
    archived_financial_period_code integer,
    archived_financial_period_name character varying(10),
    financial_year integer,
    archiving_year integer
);


CREATE TABLE IF NOT EXISTS public.dw_simulation_mi_report_previous_year_actual
(
    cost_centre_code character varying(6),
    actual_nac integer,
    programme_code character varying(50),    
    market_code character varying,
    contract_code character varying,
    project_code character varying,
    expenditure_type character varying(100),
    expenditure_type_description character varying(100),
    financial_code integer,
    previous_year_actual numeric,
    financial_period_code integer,
    financial_period_name character varying(10),
    archived_financial_period_code integer,
    archived_financial_period_name character varying(10),
    financial_year integer,
    archiving_year integer
);

CREATE TABLE IF NOT EXISTS dw_simulation_financial_period_in_use
(
    financial_period_code integer,
    period_short_name character varying(10)
);

CREATE VIEW dw_current_year_outturn as 
SELECT financial_code, coalesce(sum(actual+forecast), 0)  as current_year_outturn, archived_financial_period_code
	FROM public.dw_simulation_mi_report_forecast_actual
	GROUP BY financial_code, archived_financial_period_code;


	
CREATE VIEW dw_actual_forecast_ytd as	
SELECT financial_code, financial_period_code, archived_financial_period_code, 
sum(COALESCE(forecast, 0) + coalesce(actual, 0))  
OVER (PARTITION BY financial_code, archived_financial_period_code ORDER BY financial_period_code)
AS ytd_forecast_actual
	FROM public.dw_simulation_mi_report_forecast_actual;
	

CREATE VIEW dw_actual_ytd as
SELECT financial_code, financial_period_code, archived_financial_period_code, sum(coalesce(actual, 0)) 
OVER (PARTITION BY financial_code, archived_financial_period_code ORDER BY financial_period_code)
AS ytd_actual
	FROM public.dw_simulation_mi_report_forecast_actual
	WHERE financial_period_code <= archived_financial_period_code;
	

CREATE VIEW dw_current_rates as
    SELECT financial_code, financial_period_code, archived_financial_period_code, 
    sum(coalesce(actual, 0) + coalesce(forecast, 0))  OVER ( PARTITION BY financial_code, archived_financial_period_code ORDER BY financial_period_code) as run_rate_ytd,
    avg(coalesce(actual, 0)+ coalesce(forecast,0)) OVER (PARTITION BY financial_code, archived_financial_period_code ORDER BY financial_period_code) * 12 as full_year_run_rate
        FROM dw_simulation_mi_report_forecast_actual 
        WHERE financial_period_code <= archived_financial_period_code 
    
    UNION				 
    
     SELECT fa.financial_code, fa.financial_period_code, fa.archived_financial_period_code,    
    rate.ytd_run_rate * financial_period_code as run_rate_ytd,
    rate.ytd_run_rate * 12 as full_year_run_rate
        FROM dw_simulation_mi_report_forecast_actual fa INNER JOIN 
        (select avg(COALESCE(actual, 0) + COALESCE(forecast, 0)) as ytd_run_rate, financial_code, archived_financial_period_code
				FROM dw_simulation_mi_report_forecast_actual WHERE financial_period_code <= archived_financial_period_code 
				group by financial_code, archived_financial_period_code) as rate ON rate.financial_code = fa.financial_code and rate.archived_financial_period_code = fa.archived_financial_period_code            
        WHERE fa.financial_period_code > fa.archived_financial_period_code ;
 

CREATE VIEW dw_previous_period_forecast as 
select financial_code, coalesce(forecast, 0) as previous_period_forecast, financial_period_code
FROM dw_simulation_mi_report_forecast_actual
where financial_period_code = archived_financial_period_code+1 and archived_financial_period_code < 
(SELECT max(financial_period_code)
	FROM dw_simulation_financial_period_in_use);


"""


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunSQL(
            f"{drop_sql} {create_sql}",
            drop_sql,
        ),
    ]