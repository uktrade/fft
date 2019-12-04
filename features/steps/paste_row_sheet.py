from behave import (
    given,
    when,
    then,
)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from features.environment import (
    create_test_user,
    copy_text,
    paste,
)

from forecast.test.factories import (
    ForecastPermissionFactory,
)


@given(u'the user selects a row in the edit forecast table')
def step_impl(context):
    create_test_user(context)

    # Add forecast view permission
    ForecastPermissionFactory(
        user=context.user,
    )

    context.browser.get(f'{context.base_url}/forecast/edit/{888812}/')

    WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "select_0"))
    )

    april_value = context.browser.find_element_by_id(
        "id_Apr_0"
    ).get_attribute(
        'innerHTML'
    )

    assert april_value == "0"

    first_select = context.browser.find_element_by_id("select_0")
    first_select.click()


@when(u'the user pastes valid data')
def step_impl(context):
    no_error_paste_text = "999999	Test	1111111	2222222	3000	1000	0	0	0	0	0	0	0	0	0	0	0"
    copy_text(context, no_error_paste_text)
    paste(context)


@then(u'the clipboard data is displayed in the forecast table')
def step_impl(context):
    april_value = context.browser.find_element_by_id(
        "id_Apr_0"
    ).get_attribute(
        'innerHTML'
    )
    assert april_value == "1000"
