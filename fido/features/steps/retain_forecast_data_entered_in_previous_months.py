# -- FILE: features/steps/example_steps.py
from behave import given, when, then, step


@given('we have entered multiple months')
def step_impl(context):
    pass


@when('we look at last month')
def step_impl(context):  # -- NOTE: number is converted into integer
    pass


@then('we see last months data')
def step_impl(context):
    pass