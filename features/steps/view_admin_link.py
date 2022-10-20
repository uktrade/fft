from behave import given, then, when
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from features.environment import create_test_user


@given("I have admin site access")
def step_impl(context):
    create_test_user(context)
    context.browser.get(f"{context.base_url}/")


@when("I access the FFT website")
def step_impl(context):
    WebDriverWait(context.browser, 500).until(
        ec.presence_of_element_located((By.ID, "admin_page"))
    )


@then("I should see a link to the admin website")
def step_impl(context):
    try:
        context.browser.find_element_by_id("admin_page")
    except NoSuchElementException:
        return False
    return True
