from django.db import migrations

fields = [
    "financial_period_code",
    "period_long_name",
    "period_short_name",
    "period_calendar_code",
]

periods = [
    [1, "April", "Apr", 4],
    [2, "May", "May", 5],
    [3, "June", "Jun", 6],
    [4, "July", "Jul", 7],
    [5, "August", "Aug", 8],
    [6, "September", "Sep", 9],
    [7, "October", "Oct", 10],
    [8, "November", "Nov", 11],
    [9, "December", "Dec", 12],
    [10, "January", "Jan", 1],
    [11, "February", "Feb", 2],
    [12, "March", "Mar", 3],
    [13, "Adjustment 1", "Adj1", 0],
    [14, "Adjustment 2", "Adj2", 0],
    [15, "Adjustment 3", "Adj3", 0],
]


def populate_period(apps, schema_editor):
    PeriodModel = apps.get_model("forecast", "FinancialPeriod")
    for l in periods:
        d = dict(zip(fields, l))
        obj, created = PeriodModel.objects.get_or_create(**d)


def create_forecast_expenditure_types(apps, schema_editor):
    ForecastExpenditureType = apps.get_model("forecast", "ForecastExpenditureType")
    BudgetType = apps.get_model("chartofaccountDIT", "BudgetType")

    del_type = BudgetType.objects.get(budget_type_key="DEL")
    ame_type = BudgetType.objects.get(budget_type_key="AME")
    admin_type = BudgetType.objects.get(budget_type_key="ADMIN")

    ForecastExpenditureType.objects.create(
        forecast_expenditure_type_name="Capital",
        forecast_expenditure_type_description="Capital",
        forecast_expenditure_type_display_order=3,
        nac_economic_budget_code="CAPITAL",
        programme_budget_type=del_type,
    ).save()

    ForecastExpenditureType.objects.create(
        forecast_expenditure_type_name="Capital",
        forecast_expenditure_type_description="Capital",
        forecast_expenditure_type_display_order=3,
        nac_economic_budget_code="CAPITAL",
        programme_budget_type=ame_type,
    ).save()

    ForecastExpenditureType.objects.create(
        forecast_expenditure_type_name="Capital",
        forecast_expenditure_type_description="Capital",
        forecast_expenditure_type_display_order=3,
        nac_economic_budget_code="CAPITAL",
        programme_budget_type=admin_type,
    ).save()

    ForecastExpenditureType.objects.create(
        nac_economic_budget_code="RESOURCE",
        programme_budget_type=del_type,
        forecast_expenditure_type_name='Programme',
        forecast_expenditure_type_description='Programme Resource',
        forecast_expenditure_type_display_order=2
    ).save()

    ForecastExpenditureType.objects.create(
        nac_economic_budget_code="RESOURCE",
        programme_budget_type=ame_type,
        forecast_expenditure_type_name='Programme',
        forecast_expenditure_type_description='Programme Resource',
        forecast_expenditure_type_display_order=2
    ).save()

    ForecastExpenditureType.objects.create(
        nac_economic_budget_code="RESOURCE",
        programme_budget_type=admin_type,
        forecast_expenditure_type_name='Admin',
        forecast_expenditure_type_description='Admin Resource',
        forecast_expenditure_type_display_order=1
    ).save()


def create_forecast_lock(apps, schema_editor):
    ForecastEditState = apps.get_model('forecast', 'ForecastEditState')
    ForecastEditState.objects.create()


class Migration(migrations.Migration):
    dependencies = [("forecast", "0001_initial")]

    operations = [
        migrations.RunPython(populate_period),
        migrations.RunPython(create_forecast_expenditure_types),
        migrations.RunPython(create_forecast_lock),
        # 0038_auto_create_view_forecast_oscar_return
        migrations.RunSQL(
            """DROP VIEW  if exists "forecast_oscarreturn";
            CREATE VIEW "forecast_oscarreturn" as 

            SELECT ROW_NUMBER () OVER (ORDER BY "treasurySS_subsegment"."sub_segment_code"),
            coalesce("chartofaccountDIT_naturalcode"."account_L5_code_upload_id", "chartofaccountDIT_naturalcode"."account_L5_code_id")
            account_l5_code,
            "treasurySS_subsegment"."sub_segment_code" ,
            "treasurySS_subsegment"."sub_segment_long_name" ,                    
                       ROUND(SUM(CASE WHEN financial_period_id = 1 THEN amount ELSE NULL END)/100000) AS apr,
                       ROUND(SUM(CASE WHEN financial_period_id = 2 THEN amount ELSE NULL END)/100000) AS may,
                       ROUND(SUM(CASE WHEN financial_period_id = 3 THEN amount ELSE NULL END)/100000) AS jun,
                       ROUND(SUM(CASE WHEN financial_period_id = 4 THEN amount ELSE NULL END)/100000) AS jul,
                       ROUND(SUM(CASE WHEN financial_period_id = 5 THEN amount ELSE NULL END)/100000) AS aug,
                       ROUND(SUM(CASE WHEN financial_period_id = 6 THEN amount ELSE NULL END)/100000) AS sep,
                       ROUND(SUM(CASE WHEN financial_period_id = 7 THEN amount ELSE NULL END)/100000) AS oct,
                       ROUND(SUM(CASE WHEN financial_period_id = 8 THEN amount ELSE NULL END)/100000) AS nov,
                       ROUND(SUM(CASE WHEN financial_period_id = 9 THEN amount ELSE NULL END)/100000) AS "dec",
                       ROUND(SUM(CASE WHEN financial_period_id = 10 THEN amount ELSE NULL END)/100000) AS jan,
                       ROUND(SUM(CASE WHEN financial_period_id = 11 THEN amount ELSE NULL END)/100000) AS feb,
                       ROUND(SUM(CASE WHEN financial_period_id = 12 THEN amount ELSE NULL END)/100000) AS mar,
                       ROUND(SUM(CASE WHEN financial_period_id = 13 THEN amount ELSE NULL END)/100000) AS adj1 ,
                       ROUND(SUM(CASE WHEN financial_period_id = 14 THEN amount ELSE NULL END)/100000) AS adj2 ,
                       ROUND(SUM(CASE WHEN financial_period_id = 15 THEN amount ELSE NULL END)/100000) AS adj3
        FROM "forecast_forecastmonthlyfigure"
                INNER JOIN "forecast_financialcode" on (forecast_forecastmonthlyfigure.financial_code_id = forecast_financialcode.id)
                    LEFT OUTER JOIN "chartofaccountDIT_naturalcode"
                    ON ("forecast_financialcode"."natural_account_code_id" = "chartofaccountDIT_naturalcode"."natural_account_code")
                    INNER JOIN "costcentre_costcentre"
                    ON ("forecast_financialcode"."cost_centre_id" = "costcentre_costcentre"."cost_centre_code")
                    INNER JOIN "costcentre_directorate"
                    ON ("costcentre_costcentre"."directorate_id" = "costcentre_directorate"."directorate_code")
                    INNER JOIN "costcentre_departmentalgroup"
                    ON ("costcentre_directorate"."group_id" = "costcentre_departmentalgroup"."group_code")
                    INNER JOIN "chartofaccountDIT_programmecode" ON ("forecast_financialcode"."programme_id" = "chartofaccountDIT_programmecode"."programme_code")
                    LEFT OUTER JOIN "treasurySS_subsegment" ON ("costcentre_departmentalgroup"."treasury_segment_fk_id" = "treasurySS_subsegment"."Segment_code_id"
                    AND "chartofaccountDIT_programmecode"."budget_type_id" = "treasurySS_subsegment"."dit_budget_type_id")
                    INNER JOIN "core_financialyear" ON ("forecast_forecastmonthlyfigure"."financial_year_id" = "core_financialyear"."financial_year")
                    WHERE "core_financialyear"."current" = TRUE 
                    GROUP BY coalesce("chartofaccountDIT_naturalcode"."account_L5_code_upload_id", "chartofaccountDIT_naturalcode"."account_L5_code_id"),
                    "treasurySS_subsegment"."sub_segment_code" ;  
        """,
            'DROP VIEW "forecast_oscarreturn";',
        ),
        # 0050_auto_20200116_1204
        migrations.RunSQL("""UPDATE public."chartofaccountDIT_budgettype"
                                            SET budget_type_display_order=1
                                            WHERE budget_type_key = 'DEL';
                                        UPDATE public."chartofaccountDIT_budgettype"
                                            SET budget_type_display_order=1
                                            WHERE budget_type_key = 'ADMIN';
                                        UPDATE public."chartofaccountDIT_budgettype"
                                            SET budget_type_display_order=2
                                            WHERE budget_type_key = 'AME';
        	"""),
        # 0051_create_budget_forecast_view
        migrations.RunSQL(

            """
            DROP VIEW if exists forecast_forecast_budget_view ;
            DROP VIEW if exists yearly_budget;
            DROP VIEW if exists annual_forecast;
    
            CREATE VIEW annual_forecast as
                SELECT financial_code_id, financial_year_id,
                       SUM(CASE WHEN financial_period_id = 1 THEN amount ELSE NULL END) AS apr,
                       SUM(CASE WHEN financial_period_id = 2 THEN amount ELSE NULL END) AS may,
                       SUM(CASE WHEN financial_period_id = 3 THEN amount ELSE NULL END) AS jun,
                       SUM(CASE WHEN financial_period_id = 4 THEN amount ELSE NULL END) AS jul,
                       SUM(CASE WHEN financial_period_id = 5 THEN amount ELSE NULL END) AS aug,
                       SUM(CASE WHEN financial_period_id = 6 THEN amount ELSE NULL END) AS sep,
                       SUM(CASE WHEN financial_period_id = 7 THEN amount ELSE NULL END) AS oct,
                       SUM(CASE WHEN financial_period_id = 8 THEN amount ELSE NULL END) AS nov,
                       SUM(CASE WHEN financial_period_id = 9 THEN amount ELSE NULL END) AS "dec",
                       SUM(CASE WHEN financial_period_id = 10 THEN amount ELSE NULL END) AS jan,
                       SUM(CASE WHEN financial_period_id = 11 THEN amount ELSE NULL END) AS feb,
                       SUM(CASE WHEN financial_period_id = 12 THEN amount ELSE NULL END) AS mar,
                       SUM(CASE WHEN financial_period_id = 13 THEN amount ELSE NULL END) AS adj1 ,
                       SUM(CASE WHEN financial_period_id = 14 THEN amount ELSE NULL END) AS adj2 ,
                       SUM(CASE WHEN financial_period_id = 15 THEN amount ELSE NULL END) AS adj3
                FROM forecast_forecastmonthlyfigure
                GROUP BY financial_code_id,  financial_year_id;
    
            CREATE VIEW yearly_budget as
                SELECT financial_code_id, financial_year_id, SUM(amount) AS budget
                FROM forecast_budgetmonthlyfigure
                GROUP BY financial_code_id, financial_year_id;
    
            CREATE VIEW public.forecast_forecast_budget_view
            as
            SELECT coalesce(b.financial_code_id, f.financial_code_id) as financial_code_id,
                    coalesce(b.financial_year_id, f.financial_year_id) as financial_year,
                    coalesce(budget, 0) as budget,
                    coalesce(apr, 0) as apr,
                    coalesce(may, 0) as may,
                    coalesce(jun, 0) as jun,
                    coalesce(jul, 0) as jul,
                    coalesce(aug, 0) as aug,
                    coalesce(sep, 0) as sep,
                    coalesce(oct, 0) as oct,
                    coalesce(nov, 0) as nov,
                    coalesce("dec", 0) as "dec",
                    coalesce(jan, 0) as jan,
                    coalesce(feb, 0) as feb,
                    coalesce(mar, 0) as mar,
                    coalesce(adj1, 0) as adj1,
                    coalesce(adj2, 0) as adj2,
                    coalesce(adj3, 0) as adj3
            FROM annual_forecast f 
                FULL OUTER JOIN yearly_budget b
                    on b.financial_code_id = f.financial_code_id and b.financial_year_id = f.financial_year_id;                    
        """,
            """
                DROP VIEW if exists forecast_forecast_budget_view;
                DROP VIEW if exists yearly_budget;
                    DROP VIEW if exists annual_forecast;
                """,
        ),
        migrations.RunSQL(
            """
            DROP VIEW  if exists "forecast_oscarreturn";
            CREATE VIEW "forecast_oscarreturn" as 
    
            SELECT ROW_NUMBER () OVER (ORDER BY "treasurySS_subsegment"."sub_segment_code"),
            coalesce("chartofaccountDIT_naturalcode"."account_L5_code_upload_id", "chartofaccountDIT_naturalcode"."account_L5_code_id")
            account_l5_code,
            "treasurySS_subsegment"."sub_segment_code" ,
            "treasurySS_subsegment"."sub_segment_long_name" ,                    
                       ROUND(SUM(CASE WHEN financial_period_id = 1 THEN amount ELSE NULL END)/100000) AS apr,
                       ROUND(SUM(CASE WHEN financial_period_id = 2 THEN amount ELSE NULL END)/100000) AS may,
                       ROUND(SUM(CASE WHEN financial_period_id = 3 THEN amount ELSE NULL END)/100000) AS jun,
                       ROUND(SUM(CASE WHEN financial_period_id = 4 THEN amount ELSE NULL END)/100000) AS jul,
                       ROUND(SUM(CASE WHEN financial_period_id = 5 THEN amount ELSE NULL END)/100000) AS aug,
                       ROUND(SUM(CASE WHEN financial_period_id = 6 THEN amount ELSE NULL END)/100000) AS sep,
                       ROUND(SUM(CASE WHEN financial_period_id = 7 THEN amount ELSE NULL END)/100000) AS oct,
                       ROUND(SUM(CASE WHEN financial_period_id = 8 THEN amount ELSE NULL END)/100000) AS nov,
                       ROUND(SUM(CASE WHEN financial_period_id = 9 THEN amount ELSE NULL END)/100000) AS "dec",
                       ROUND(SUM(CASE WHEN financial_period_id = 10 THEN amount ELSE NULL END)/100000) AS jan,
                       ROUND(SUM(CASE WHEN financial_period_id = 11 THEN amount ELSE NULL END)/100000) AS feb,
                       ROUND(SUM(CASE WHEN financial_period_id = 12 THEN amount ELSE NULL END)/100000) AS mar,
                       ROUND(SUM(CASE WHEN financial_period_id = 13 THEN amount ELSE NULL END)/100000) AS adj1 ,
                       ROUND(SUM(CASE WHEN financial_period_id = 14 THEN amount ELSE NULL END)/100000) AS adj2 ,
                       ROUND(SUM(CASE WHEN financial_period_id = 15 THEN amount ELSE NULL END)/100000) AS adj3
        FROM "forecast_forecastmonthlyfigure"
                INNER JOIN "forecast_financialcode" on (forecast_forecastmonthlyfigure.financial_code_id = forecast_financialcode.id)
                    LEFT OUTER JOIN "chartofaccountDIT_naturalcode"
                    ON ("forecast_financialcode"."natural_account_code_id" = "chartofaccountDIT_naturalcode"."natural_account_code")
                    INNER JOIN "costcentre_costcentre"
                    ON ("forecast_financialcode"."cost_centre_id" = "costcentre_costcentre"."cost_centre_code")
                    INNER JOIN "costcentre_directorate"
                    ON ("costcentre_costcentre"."directorate_id" = "costcentre_directorate"."directorate_code")
                    INNER JOIN "costcentre_departmentalgroup"
                    ON ("costcentre_directorate"."group_id" = "costcentre_departmentalgroup"."group_code")
                    INNER JOIN "chartofaccountDIT_programmecode" ON ("forecast_financialcode"."programme_id" = "chartofaccountDIT_programmecode"."programme_code")
                    LEFT OUTER JOIN "treasurySS_subsegment" ON ("costcentre_departmentalgroup"."treasury_segment_fk_id" = "treasurySS_subsegment"."Segment_code_id"
                    AND "chartofaccountDIT_programmecode"."budget_type_id" = "treasurySS_subsegment"."dit_budget_type_id")
                    INNER JOIN "core_financialyear" ON ("forecast_forecastmonthlyfigure"."financial_year_id" = "core_financialyear"."financial_year")
                    WHERE "core_financialyear"."current" = TRUE 
                    AND "forecast_forecastmonthlyfigure"."archived_status_id" is NULL
                    GROUP BY coalesce("chartofaccountDIT_naturalcode"."account_L5_code_upload_id", "chartofaccountDIT_naturalcode"."account_L5_code_id"),
                    "treasurySS_subsegment"."sub_segment_code" ;  
        """,
        ),
        migrations.RunSQL(
            """
            DROP VIEW if exists forecast_forecast_budget_view CASCADE;
            DROP VIEW if exists yearly_budget CASCADE;
            DROP VIEW if exists annual_forecast CASCADE;
    
            CREATE VIEW annual_forecast as
                SELECT financial_code_id, financial_year_id,
                       SUM(CASE WHEN financial_period_id = 1 THEN amount ELSE NULL END) AS apr,
                       SUM(CASE WHEN financial_period_id = 2 THEN amount ELSE NULL END) AS may,
                       SUM(CASE WHEN financial_period_id = 3 THEN amount ELSE NULL END) AS jun,
                       SUM(CASE WHEN financial_period_id = 4 THEN amount ELSE NULL END) AS jul,
                       SUM(CASE WHEN financial_period_id = 5 THEN amount ELSE NULL END) AS aug,
                       SUM(CASE WHEN financial_period_id = 6 THEN amount ELSE NULL END) AS sep,
                       SUM(CASE WHEN financial_period_id = 7 THEN amount ELSE NULL END) AS oct,
                       SUM(CASE WHEN financial_period_id = 8 THEN amount ELSE NULL END) AS nov,
                       SUM(CASE WHEN financial_period_id = 9 THEN amount ELSE NULL END) AS "dec",
                       SUM(CASE WHEN financial_period_id = 10 THEN amount ELSE NULL END) AS jan,
                       SUM(CASE WHEN financial_period_id = 11 THEN amount ELSE NULL END) AS feb,
                       SUM(CASE WHEN financial_period_id = 12 THEN amount ELSE NULL END) AS mar,
                       SUM(CASE WHEN financial_period_id = 13 THEN amount ELSE NULL END) AS adj1 ,
                       SUM(CASE WHEN financial_period_id = 14 THEN amount ELSE NULL END) AS adj2 ,
                       SUM(CASE WHEN financial_period_id = 15 THEN amount ELSE NULL END) AS adj3
                FROM forecast_forecastmonthlyfigure
                    WHERE forecast_forecastmonthlyfigure.archived_status_id is NULL
                GROUP BY financial_code_id,  financial_year_id;
    
            CREATE VIEW yearly_budget as
                SELECT financial_code_id, financial_year_id, archived_status_id, SUM(amount) AS budget
                FROM forecast_budgetmonthlyfigure
                    WHERE forecast_budgetmonthlyfigure.archived_status_id is NULL
                GROUP BY financial_code_id, financial_year_id, archived_status_id;
    
            CREATE VIEW public.forecast_forecast_budget_view
            as
            SELECT coalesce(b.financial_code_id, f.financial_code_id) as financial_code_id,
                    coalesce(b.financial_year_id, f.financial_year_id) as financial_year,
                    coalesce(budget, 0) as budget,
                    coalesce(apr, 0) as apr,
                    coalesce(may, 0) as may,
                    coalesce(jun, 0) as jun,
                    coalesce(jul, 0) as jul,
                    coalesce(aug, 0) as aug,
                    coalesce(sep, 0) as sep,
                    coalesce(oct, 0) as oct,
                    coalesce(nov, 0) as nov,
                    coalesce("dec", 0) as "dec",
                    coalesce(jan, 0) as jan,
                    coalesce(feb, 0) as feb,
                    coalesce(mar, 0) as mar,
                    coalesce(adj1, 0) as adj1,
                    coalesce(adj2, 0) as adj2,
                    coalesce(adj3, 0) as adj3
            FROM annual_forecast f 
                FULL OUTER JOIN yearly_budget b
                    on b.financial_code_id = f.financial_code_id and b.financial_year_id = f.financial_year_id;                    
         """,
        ),
    ]
