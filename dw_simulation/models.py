"""

UPDATE dw_simulation_mi_report_previous_year_actual
    SET
        previous_year_actual =
        dw_simulation_mi_report_previous_year_actual.previous_year_actual
            + t1.previous_year_actual
            + t2.previous_year_actual
            + t3.previous_year_actual
    from
    (SELECT previous_year_actual, financial_period_code,
    financial_code, archived_financial_period_code
     FROM dw_simulation_mi_report_previous_year_actual) t1,
    (SELECT previous_year_actual, financial_period_code,
    financial_code, archived_financial_period_code
     FROM dw_simulation_mi_report_previous_year_actual) t2,
    (SELECT previous_year_actual, financial_period_code,
    financial_code, archived_financial_period_code
     FROM dw_simulation_mi_report_previous_year_actual) t3
    WHERE dw_simulation_mi_report_previous_year_actual.financial_code
    = t1.financial_code
    AND dw_simulation_mi_report_previous_year_actual.financial_code = t2.financial_code
    AND dw_simulation_mi_report_previous_year_actual.financial_code = t3.financial_code
    AND dw_simulation_mi_report_previous_year_actual.archived_financial_period_code
    = t1.archived_financial_period_code
    AND dw_simulation_mi_report_previous_year_actual.archived_financial_period_code
    = t2.archived_financial_period_code
    AND dw_simulation_mi_report_previous_year_actual.archived_financial_period_code
    = t3.archived_financial_period_code
    AND dw_simulation_mi_report_previous_year_actual.financial_period_code = 12
    AND t1.financial_period_code = 13
    AND t2.financial_period_code = 14
    AND t3.financial_period_code = 15;

DELETE FROM dw_simulation_mi_report_previous_year_actual
WHERE financial_period_code > 12;

UPDATE dw_simulation_mi_report_budget
    SET
        budget = dw_simulation_mi_report_budget.budget
            + t1.budget + t2.budget + t3.budget
    from
    (SELECT budget, financial_period_code,
    financial_code, archived_financial_period_code
     FROM dw_simulation_mi_report_budget) t1,
    (SELECT budget, financial_period_code,
    financial_code, archived_financial_period_code
     FROM dw_simulation_mi_report_budget) t2,
    (SELECT budget, financial_period_code,
    financial_code, archived_financial_period_code
     FROM dw_simulation_mi_report_budget) t3
    WHERE dw_simulation_mi_report_budget.financial_code = t1.financial_code
    AND dw_simulation_mi_report_budget.financial_code = t2.financial_code
    AND dw_simulation_mi_report_budget.financial_code = t3.financial_code
    AND dw_simulation_mi_report_budget.archived_financial_period_code
    = t1.archived_financial_period_code
    AND dw_simulation_mi_report_budget.archived_financial_period_code
    = t2.archived_financial_period_code
    AND dw_simulation_mi_report_budget.archived_financial_period_code
    = t3.archived_financial_period_code
    AND dw_simulation_mi_report_budget.financial_period_code = 12
    AND t1.financial_period_code = 13
    AND t2.financial_period_code = 14
    AND t3.financial_period_code = 15;

DELETE FROM dw_simulation_mi_report_budget WHERE financial_period_code > 12;


UPDATE dw_simulation_mi_report_forecast_actual
    SET
        forecast = dw_simulation_mi_report_forecast_actual.forecast
            + t1.forecast + t2.forecast + t3.actual,
        actual = dw_simulation_mi_report_forecast_actual.actual
            + t1.actual + t2.actual + t3.actual
    from
    (SELECT actual, forecast,  financial_period_code,
    financial_code, archived_financial_period_code
     FROM dw_simulation_mi_report_forecast_actual) t1,
    (SELECT actual, forecast,  financial_period_code,
    financial_code, archived_financial_period_code
     FROM dw_simulation_mi_report_forecast_actual) t2,
    (SELECT actual, forecast,  financial_period_code,
    financial_code, archived_financial_period_code
     FROM dw_simulation_mi_report_forecast_actual) t3
    WHERE dw_simulation_mi_report_forecast_actual.financial_code = t1.financial_code
    AND dw_simulation_mi_report_forecast_actual.financial_code = t2.financial_code
    AND dw_simulation_mi_report_forecast_actual.financial_code = t3.financial_code
    AND dw_simulation_mi_report_forecast_actual.archived_financial_period_code =
    t1.archived_financial_period_code
    AND dw_simulation_mi_report_forecast_actual.archived_financial_period_code =
    t2.archived_financial_period_code
    AND dw_simulation_mi_report_forecast_actual.archived_financial_period_code =
    t3.archived_financial_period_code
    AND dw_simulation_mi_report_forecast_actual.financial_period_code = 12
    AND t1.financial_period_code = 13
    AND t2.financial_period_code = 14
    AND t3.financial_period_code = 15;

DELETE FROM dw_simulation_mi_report_forecast_actual WHERE financial_period_code > 12;



"""
