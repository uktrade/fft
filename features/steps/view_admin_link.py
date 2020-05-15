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


@given(u'I have admin site access')
def step_impl(context):
    create_test_user(context)
    context.browser.get(f'{context.base_url}/')


@when(u'I access the FFT website')
def step_impl(context):
    WebDriverWait(context.browser, 500).until(
        ec.presence_of_element_located((By.ID, "admin_page"))
    )


@then(u'I should see a link to the admin website')
def step_impl(context):
    try:
        context.browser.find_element_by_id(
            "admin_page"
        )
    except NoSuchElementException:
        return False
    return True

