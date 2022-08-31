"""

UPDATE dw_simulation_mi_report_previous_year_actual
    SET
        previous_year_actual =
        coalesce(dw_simulation_mi_report_previous_year_actual.previous_year_actual, 0)
        coalesce(t1.previous_year_actual, 0)
        coalesce(t2.previous_year_actual, 0)
        coalesce(t3.previous_year_actual, 0)
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






"""
