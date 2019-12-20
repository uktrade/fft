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
    create_test_user,
)

from forecast.test.factories import (
    ForecastPermissionFactory,
)


@given(u'the user wants to hide the NAC column')
def step_impl(context):
    create_test_user(context)

    # Add forecast view permission
    ForecastPermissionFactory(
        user=context.user,
    )

    context.browser.get(f'{context.base_url}/forecast/edit/{888812}/')


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
