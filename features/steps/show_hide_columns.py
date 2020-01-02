from behave import (
    given,
    when,
    then,
)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException

from features.environment import (
    TEST_COST_CENTRE_CODE,
    create_test_user,
)


@given(u'the user wants to hide the NAC column')
def step_impl(context):
    create_test_user(context)
    context.browser.get(f'{context.base_url}/forecast/edit/{TEST_COST_CENTRE_CODE}/')


@when(u'the user clicks the hide NAC column')
def step_impl(context):
    WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "show_hide_nac"))
    )

    show_hide_nac = context.browser.find_element_by_id("show_hide_nac")
    show_hide_nac.click()


@then(u'the NAC column is hidden')
def step_impl(context):
    header_hidden = False

    try:
        context.browser.find_element_by_id("natural_account_code_header")
    except NoSuchElementException:
        header_hidden = True

    assert header_hidden
