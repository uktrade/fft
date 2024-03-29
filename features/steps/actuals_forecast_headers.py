from behave import given, then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from features.environment import TEST_COST_CENTRE_CODE, create_test_user
from forecast.models import FinancialPeriod


@given("the user views the edit forecast page with six months of actuals")
def step_impl(context):

    for i in range(1, 7):
        actual = FinancialPeriod.objects.get(financial_period_code=i)
        actual.actual_loaded = True
        actual.save()

    create_test_user(context)

    context.browser.get(f"{context.base_url}/forecast/edit/{TEST_COST_CENTRE_CODE}/")


@when("the user checks the actuals columns")
def step_impl(context):

    WebDriverWait(context.browser, 500).until(
        ec.presence_of_element_located((By.ID, "actuals_header"))
    )


@then("there are six actuals columns")
def step_impl(context):
    actuals_header = context.browser.find_element(By.ID, "actuals_header")

    actuals_colspan = actuals_header.get_attribute("colspan")

    assert actuals_colspan == "6"


@given("the user views the edit forecast page with three months of actuals")
def step_impl(context):

    for i in range(1, 4):
        actual = FinancialPeriod.objects.get(financial_period_code=i)
        actual.actual_loaded = True
        actual.save()

    create_test_user(context)

    context.browser.get(f"{context.base_url}/forecast/edit/{TEST_COST_CENTRE_CODE}/")


@then("there are three actuals columns")
def step_impl(context):
    actuals_header = context.browser.find_element(By.ID, "actuals_header")

    actuals_colspan = actuals_header.get_attribute("colspan")

    assert actuals_colspan == "3"
