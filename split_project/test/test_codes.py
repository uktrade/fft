from django.db.models import Sum

from forecast.models import (
    ForecastMonthlyFigure,
)
from split_project.split_figure import (
    PAY_CODE,
    calculate_expenditure_type_total,
    handle_split_project,
)

from split_project.test.test_utils import (
    SplitDataSetup,
    create_split_data,
    create_monthly_amount,
)


class SplitDataTest(SplitDataSetup):
    def setUp(self):
        super().setUp()

        create_split_data(
            self.cost_centre_code1,
            self.natural_account_code_pay1,
            self.programme_code,
            self.project_code1,
            6785,
            self.period_obj,
        )
        create_split_data(
            self.cost_centre_code,
            self.natural_account_code_pay2,
            self.programme_code,
            self.project_code2,
            215,
            self.period_obj,
        )
        create_split_data(
            self.cost_centre_code,
            self.natural_account_code_pay,
            self.programme_code,
            self.project_code3,
            3000,
            self.period_obj,
        )

        test_pay_amount = 987654321
        amount1 = 10000
        amount2 = 15000
        test_pay_amount1 = 1234555

        # Create the amount to be split
        create_monthly_amount(
            self.cost_centre_code,
            self.natural_account_code_pay,
            self.programme_code,
            self.project_code3,
            test_pay_amount,
            self.period_obj,
        )

        create_monthly_amount(
            self.cost_centre_code,
            self.natural_account_code_non_pay,
            self.programme_code,
            self.project_code3,
            amount1,
            self.period_obj,
        )

        create_monthly_amount(
            self.cost_centre_code1,
            self.natural_account_code_non_pay,
            self.programme_code,
            self.project_code3,
            amount2,
            self.period_obj,
        )
        create_monthly_amount(
            self.cost_centre_code_different_directorate,
            self.natural_account_code_pay,
            self.programme_code,
            self.project_code3,
            test_pay_amount1,
            self.period_obj,
        )

        self.total_amount = test_pay_amount + amount1 + amount2 + test_pay_amount1

    def test_split_pay(self):

        self.assertEqual(
            ForecastMonthlyFigure.objects.filter(
                financial_code__cost_centre=self.cost_centre_code,
            ).count(),
            2,
        )
        spend_directorate_before = calculate_expenditure_type_total(
            self.directorate_code,
            self.test_period,
            PAY_CODE,
        )
        spend_directorate1_before = calculate_expenditure_type_total(
            self.directorate_code1,
            self.test_period,
            PAY_CODE,
        )

        handle_split_project(self.period_obj.financial_period_code)

        spend_directorate_after = calculate_expenditure_type_total(
            self.directorate_code,
            self.test_period,
            PAY_CODE,
        )
        spend_directorate1_after = calculate_expenditure_type_total(
            self.directorate_code1,
            self.test_period,
            PAY_CODE,
        )

        # Check that the total for pay has not changed
        self.assertEqual(spend_directorate_before, spend_directorate_after)
        self.assertEqual(spend_directorate1_before, spend_directorate1_after)

        # Check for existence of monthly figures: 2 created,
        # and 1 created by splitting by project code
        self.assertEqual(
            ForecastMonthlyFigure.objects.filter(
                financial_code__cost_centre=self.cost_centre_code
            ).count(),
            3,
        )

        result = ForecastMonthlyFigure.objects.all().aggregate(total=Sum("amount"))
        self.assertEqual(
            result["total"], self.total_amount,
        )
