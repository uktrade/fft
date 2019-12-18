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

from forecast.models import (
    FinancialPeriod,
)

from forecast.test.factories import (
    ForecastPermissionFactory,
)


def check_error_message(context, msg):
    WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "paste_error_msg"))
    )
    error_msg = context.browser.find_element_by_id(
        "paste_error_msg"
    ).get_attribute(
        'innerHTML'
    )

    assert error_msg == msg


@given(u'the user selects all rows in the edit forecast table')
def step_impl(context):
    create_test_user(context)

    # Add forecast view permission
    ForecastPermissionFactory(
        user=context.user,
    )

    context.browser.get(f'{context.base_url}/forecast/edit/{888812}/')

    WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "id_apr_0"))
    )

    april_value = context.browser.find_element_by_id(
        "id_apr_0"
    ).get_attribute(
        'innerHTML'
    )

    assert april_value == "0"

    WebDriverWait(context.browser, 5000).until(
        ec.presence_of_element_located((By.ID, "select_all"))
    )

    first_select = context.browser.find_element_by_id("select_all")
    first_select.click()


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
        "id_apr_0"
    ).get_attribute(
        'innerHTML'
    )

    assert april_value == "0"

    first_select = context.browser.find_element_by_id("select_0")
    first_select.click()


@when(u'the user pastes valid row data')
def step_impl(context):
    paste_text = "999999	123456	1111111	2222222	3000	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00"
    copy_text(context, paste_text)
    paste(context)


@when(u'the user pastes valid sheet data')
def step_impl(context):
    paste_text = "999999	123456	1111111	2222222	3000	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00\\n111111	123456	1111111	2222222	3000	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00"

    copy_text(context, paste_text)
    paste(context)


@when(u'the user pastes too many rows')
def step_impl(context):
    too_many_rows_paste_text = "999999	123456	1111111	2222222	3000	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00\\n111111	123456	1111111	2222222	3000	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00\\n222222	123456	1111111	2222222	3000	1000.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00"
    copy_text(context, too_many_rows_paste_text)
    paste(context)


@then(u'the clipboard data is displayed in the forecast table')
def step_impl(context):
    april_value = context.browser.find_element_by_id(
        "id_apr_0"
    ).get_attribute(
        'innerHTML'
    )

    assert april_value == "1,000"


@when(u'the user pastes invalid row data')
def step_impl(context):
    error_paste_text = "This is a mistake..."
    copy_text(context, error_paste_text)
    paste(context)


@then(u'the incorrect format error is displayed')
def step_impl(context):
    check_error_message(
        context,
        "Your pasted data is not in the correct format",
    )


@then('the too few rows error is displayed')
def step_impl(context):
    check_error_message(
        context,
        "You have selected all forecast rows but the pasted data has too few rows.",
    )


@then('the too many rows error is displayed')
def step_impl(context):
    check_error_message(
        context,
        "You have selected all forecast rows but the pasted data has too many rows.",
    )


@when(u'the user pastes valid row data with actuals changed')
def step_impl(context):
    april = FinancialPeriod.objects.filter(
        period_long_name="April"
    ).first()
    april.actual_loaded = True
    april.save()

    paste_text = "999999	123456	1111111	2222222	3000	111.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00"
    copy_text(context, paste_text)
    paste(context)

    april.actual_loaded = False
    april.save()


@then(u'the actuals data is unchanged')
def step_impl(context):
    april_value = context.browser.find_element_by_id(
        "id_apr_0"
    ).get_attribute(
        'innerHTML'
    )
    assert april_value == "0"


@when(u'the user pastes valid row data with a 5 decimal place value')
def step_impl(context):
    paste_text = "999999	123456	1111111	2222222	3000	1000.49999	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00"
    copy_text(context, paste_text)
    paste(context)


@when(u'the user pastes too many column row data')
def step_impl(context):
    paste_text = "999999	123456	1111111	2222222	3000	1000.49999	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00"
    copy_text(context, paste_text)
    paste(context)


@then(u'the too many columns error message is displayed')
def step_impl(context):
    check_error_message(
        context,
        'Your pasted data does not '
        'match the expected format. '
        'There are too many columns.'
    )


@when(u'the user pastes too few column row data')
def step_impl(context):
    paste_text = "999999	123456	1111111	2222222	3000	1000.49999	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00"
    copy_text(context, paste_text)
    paste(context)


@then(u'the too few columns error message is displayed')
def step_impl(context):
    check_error_message(
        context,
        'Your pasted data does not '
        'match the expected format. '
        'There are not enough columns.'
    )


@when(u'the user pastes mismatched columns')
def step_impl(context):
    paste_text = "333444	123456	1111111	2222222	3000	1000.49999	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00"
    copy_text(context, paste_text)
    paste(context)


@then(u'the mismatched columns error message is displayed')
def step_impl(context):
    check_error_message(
        context,
        'There is a mismatch between your pasted and selected rows. Please check the following columns: "Natural account code".'
    )
