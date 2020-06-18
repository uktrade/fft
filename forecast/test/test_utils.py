from forecast.models import (
    BudgetMonthlyFigure,
    FinancialPeriod,
)


def create_budget(financial_code_obj, year_obj):
    budget_apr = 1000000
    budget_may = -1234567
    budget_july = 1234567
    budget_total = budget_apr + budget_may + budget_july
    # Save several months, and check that the total is displayed
    apr_budget = BudgetMonthlyFigure.objects.create(
        financial_period=FinancialPeriod.objects.get(
            financial_period_code=1
        ),
        financial_code=financial_code_obj,
        financial_year=year_obj,
        amount=budget_apr
    )
    apr_budget.save
    may_budget = BudgetMonthlyFigure.objects.create(
        financial_period=FinancialPeriod.objects.get(
            financial_period_code=2,
        ),
        amount=budget_may,
        financial_code=financial_code_obj,
        financial_year=year_obj
    )
    may_budget.save
    july_budget = BudgetMonthlyFigure.objects.create(
        financial_period=FinancialPeriod.objects.get(
            financial_period_code=4,
        ),
        amount=budget_july,
        financial_code=financial_code_obj,
        financial_year=year_obj
    )
    july_budget.save
    return budget_total


def format_forecast_figure(value):
    return f'{round(value):,d}'
