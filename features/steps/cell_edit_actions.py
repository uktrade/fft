import time

from behave import (
    given,
    when,
    then,
)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec

from selenium.webdriver.common.action_chains import ActionChains

from features.environment import (
    TEST_COST_CENTRE_CODE,
    create_test_user,
)


@given(u'the user wants to edit a cell value')
def step_impl(context):
    create_test_user(context)
    context.browser.get(f'{context.base_url}/forecast/edit/{TEST_COST_CENTRE_CODE}/')


@when(u'the user double clicks an editable cell in the edit forecast table')
def step_impl(context):
    WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "id_6_0"))
    )

    june_cell = context.browser.find_element_by_id("id_6_0")
    action_chains = ActionChains(context.browser)
    action_chains.double_click(june_cell).perform()


@when(u'the user tabs to a cell')
def step_impl(context):
    may_cell = WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "id_5_0"))
    )

    action_chains = ActionChains(context.browser)
    action_chains.double_click(may_cell).perform()

    action_chains = ActionChains(context.browser)
    action_chains.key_down(Keys.TAB).perform()


@then(u'the cell becomes editable')
def step_impl(context):
    june_cell_input_value = WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "id_6_0_input"))
    ).get_attribute(
        'value'
    )

    assert june_cell_input_value == "0.00"


@given(u'the user edits a cell value')
def step_impl(context):
    create_test_user(context)
    context.browser.get(f'{context.base_url}/forecast/edit/{TEST_COST_CENTRE_CODE}/')

    WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "id_6_0"))
    )

    june_cell = context.browser.find_element_by_id("id_6_0")
    action_chains = ActionChains(context.browser)
    action_chains.double_click(june_cell).perform()

    june_input = WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "id_6_0_input"))
    )

    action_chains = ActionChains(context.browser)
    action_chains.double_click(june_input).perform()

    june_input.send_keys("1")
    june_input.send_keys("0")
    june_input.send_keys("0")
    june_input.send_keys("0")
    june_input.send_keys("0")


@when(u'the user tabs to a new cell')
def step_impl(context):
    action_chains = ActionChains(context.browser)
    action_chains.key_down(Keys.TAB).perform()


@then(u'the value is changed and has the correct format')
def step_impl(context):
    june_cell = WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "id_6_0"))
    )

    cell_value = june_cell.get_attribute(
        'innerHTML'
    )

    assert cell_value == "10,000"


@when(u'the user shift tabs to the previous cell')
def step_impl(context):
    action_chains = ActionChains(context.browser)
    action_chains.key_down(Keys.SHIFT).key_down(Keys.TAB).perform()


@then(u'the previous cell is in edit mode')
def step_impl(context):
    WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "id_5_0_input"))
    )
