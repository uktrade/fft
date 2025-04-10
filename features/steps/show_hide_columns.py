from behave import given, then, when
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from features.environment import TEST_COST_CENTRE_CODE, create_test_user


@given("the user wants to hide the NAC code column")
def step_impl(context):
    create_test_user(context)
    context.browser.get(f"{context.base_url}/forecast/edit/{TEST_COST_CENTRE_CODE}/")


@when("the user clicks the hide NAC code column")
def step_impl(context):
    filter_switch_button = WebDriverWait(context.browser, 500).until(
        ec.presence_of_element_located((By.ID, "action-bar-switch"))
    )

    filter_switch_button.click()

    show_hide_nac_code = WebDriverWait(context.browser, 500).until(
        ec.presence_of_element_located((By.ID, "show_hide_nac_code"))
    )
    show_hide_nac_code.click()


@then("the NAC code column is hidden")
def step_impl(context):
    header_hidden = False

    try:
        WebDriverWait(context.browser, 5).until(
            ec.presence_of_element_located((By.ID, "natural_account_code_header"))
        )
    except TimeoutException:
        header_hidden = True

    assert header_hidden
