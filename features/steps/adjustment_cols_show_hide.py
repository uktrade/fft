from behave import (
    given,
    when,
    then,
)

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from features.environment import (
    TEST_COST_CENTRE_CODE,
    create_test_user,
)

from forecast.models import FinancialPeriod, FinancialCode
from forecast.test.factories import (
    FinancialCodeFactory,
    FinancialPeriodFactory,
)

@given(u'adjustment 1 is set to display')
def step_impl(context):

    financial_period = FinancialPeriod.objects.filter(
        financial_period_code=13,
    ).first()

    if not financial_period:
        FinancialPeriodFactory(
            financial_period_code=13,
            period_long_name="Adjustment 1",
            period_short_name="adj1",
            period_calendar_code=16,
            display_figure=True,
        )
    else:
        financial_period.display_figure = True
        financial_period.save()


@given(u'adjustment 1 is set to hide')
def step_impl(context):
    financial_period = FinancialPeriod.objects.filter(
        financial_period_code=13,
    ).first()

    if not financial_period:
        FinancialPeriodFactory(
            financial_period_code=13,
            period_long_name="Adjustment 1",
            period_short_name="adj1",
            period_calendar_code=16,
            display_figure=False,
        )
    else:
        financial_period.display_figure = False
        financial_period.save()


@when(u'the user views the edit forecast page')
def step_impl(context):
    create_test_user(context)

    context.browser.get(
        f'{context.base_url}/forecast/edit/{TEST_COST_CENTRE_CODE}/'
    )


@then(u'the adjustment 1 column is shown')
def step_impl(context):
    WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "id_0_13"))
    )


@then(u'the adjustment 1 column is hidden')
def step_impl(context):
    adjustment_1_hidden = False

    try:
        context.browser.find_element_by_id("id_0_13")
    except NoSuchElementException:
        adjustment_1_hidden = True

    assert adjustment_1_hidden
