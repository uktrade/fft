from behave import given, when, then, step
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import (
#     click_and_hold,
#     move_to_element,
#     release,
# )


@given(u'the user pastes into the edit forecast table')
def step_impl(context):

    #context.browser.get("https://www.google.com")

    # br = context.browser
    # br.open(context.browser_url('/forecast/edit/'))

    context.browser.get("http://localhost:8000/forecast/edit/")

    WebDriverWait(context.browser, 30).until(
        EC.presence_of_element_located((By.ID, "forecast-table"))
    )

    table_cells = context.browser.find_element_by_css_selector('td.no-select')

    print(table_cells)

    # click_and_hold()
    #
    # move_to_element(toElement)
    #
    # release()


@when(u'the user checks the forecast table')
def step_impl(context):
    raise NotImplementedError(u'STEP: When the user checks the forecast table')


@then(u'the clipboard data is displayed')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the clipboard data is displayed')
