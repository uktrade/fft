from behave import (
    then,
)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


@then(u'the totals are updated')
def step_impl(context):
    # Year to date and year total
    year_to_date_value = WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "to_date_total_0"))
    ).get_attribute(
        'innerHTML'
    )

    year_total_row_0_value = WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "year_total_0"))
    ).get_attribute(
        'innerHTML'
    )

    assert year_to_date_value == "0"
    assert year_total_row_0_value == "10,000"

    # Column

    col_5_total_value = WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "col_total_5"))
    ).get_attribute(
        'innerHTML'
    )

    col_6_total_value = WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "col_total_6"))
    ).get_attribute(
        'innerHTML'
    )

    assert col_5_total_value == "0"
    assert col_6_total_value == "10,000"

    # Overspend/underspend
    ou_0_value = WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "ou_spend_0"))
    ).get_attribute(
        'innerHTML'
    )

    assert ou_0_value == "-10,000"

    ou_total_value = WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "overspend-underspend-total"))
    ).get_attribute(
        'innerHTML'
    )

    assert ou_total_value == "-10,000"
