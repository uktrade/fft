from forecast.models import BudgetMonthlyFigure, FinancialPeriod


TOTAL_COLUMN = -5
SPEND_TO_DATE_COLUMN = -2
UNDERSPEND_COLUMN = -4

HIERARCHY_TABLE_INDEX = 0
PROGRAMME_TABLE_INDEX = 1
EXPENDITURE_TABLE_INDEX = 2
PROJECT_TABLE_INDEX = 3


def create_budget(financial_code_obj, year_obj):
    budget_apr = 1000000
    budget_may = -1234567
    budget_july = 1234567
    budget_total = budget_apr + budget_may + budget_july
    # Save several months, and check that the total is displayed
    # apr figure
    BudgetMonthlyFigure.objects.create(
        financial_period=FinancialPeriod.objects.get(financial_period_code=1),
        financial_code=financial_code_obj,
        financial_year=year_obj,
        amount=budget_apr,
    )
    # may budget
    BudgetMonthlyFigure.objects.create(
        financial_period=FinancialPeriod.objects.get(
            financial_period_code=2,
        ),
        amount=budget_may,
        financial_code=financial_code_obj,
        financial_year=year_obj,
    )
    # july budget
    BudgetMonthlyFigure.objects.create(
        financial_period=FinancialPeriod.objects.get(
            financial_period_code=4,
        ),
        amount=budget_july,
        financial_code=financial_code_obj,
        financial_year=year_obj,
    )
    return budget_total


def format_forecast_figure(value):
    return f"{round(value):,d}"
