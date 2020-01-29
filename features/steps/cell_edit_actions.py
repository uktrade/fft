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
        ec.presence_of_element_located((By.ID, "id_0_6"))
    )

    sept_cell = context.browser.find_element_by_id("id_0_6")
    action_chains = ActionChains(context.browser)
    action_chains.double_click(sept_cell).perform()


@when(u'the user tabs to a cell')
def step_impl(context):
    aug_cell = WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "id_0_5"))
    )

    action_chains = ActionChains(context.browser)
    action_chains.double_click(aug_cell).perform()

    action_chains = ActionChains(context.browser)
    action_chains.key_down(Keys.TAB).perform()


@then(u'the cell becomes editable')
def step_impl(context):
    sept_cell_input_value = WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "id_0_6_input"))
    ).get_attribute(
        'value'
    )

    assert sept_cell_input_value == "0.00"


@given(u'the user edits a cell value')
def step_impl(context):
    create_test_user(context)
    context.browser.get(f'{context.base_url}/forecast/edit/{TEST_COST_CENTRE_CODE}/')

    WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "id_0_6"))
    )

    sept_cell = context.browser.find_element_by_id("id_0_6")
    action_chains = ActionChains(context.browser)
    action_chains.double_click(sept_cell).perform()

    sept_input = WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "id_0_6_input"))
    )

    action_chains = ActionChains(context.browser)
    action_chains.double_click(sept_input).perform()

    sept_input.send_keys("1")
    sept_input.send_keys("0")
    sept_input.send_keys("0")
    sept_input.send_keys("0")
    sept_input.send_keys("0")


@when(u'the user tabs to a new cell')
def step_impl(context):
    action_chains = ActionChains(context.browser)
    action_chains.key_down(Keys.TAB).perform()


@then(u'the value is changed and has the correct format')
def step_impl(context):
    sept_cell = WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "id_0_6"))
    )
    cell_value = sept_cell.get_attribute(
        'innerHTML'
    )
    assert cell_value == "10,000"

    # Check that cell has edited class
    classes = sept_cell.get_attribute("class")
    class_list = classes.split(" ")
    assert "edited" in class_list


@when(u'the user shift tabs to the previous cell')
def step_impl(context):
    action_chains = ActionChains(context.browser)
    action_chains.key_down(Keys.SHIFT).key_down(Keys.TAB).perform()


@then(u'the previous cell is in edit mode')
def step_impl(context):
    WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "id_0_5_input"))
    )
