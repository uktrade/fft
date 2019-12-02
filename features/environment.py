from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from django.conf import settings

from django.contrib.auth import get_user_model


# def django_ready(context, scenario):
#     # This function is run inside the transaction
#     test_user_email = "test@test.com"
#     test_password = "test_password"
#
#     test_user, _ = get_user_model().objects.get_or_create(
#         email=test_user_email
#     )
#     test_user.set_password(test_password)
#     test_user.save()
#
#     context.user = test_user
from behave_django.testcase import BehaviorDrivenTestCase


def before_scenario(context, scenario):
    #BehaviorDrivenTestCase.port = 8801
    BehaviorDrivenTestCase.host = 'fido'
    #context.test.port = 8001


def before_feature(context, feature):
    context.browser = webdriver.Remote(
        command_executor="http://{}:4444/wd/hub".format(
            settings.SELENIUM_ADDRESS
        ),
        desired_capabilities=DesiredCapabilities.CHROME,
    )
    context.browser.implicitly_wait(5)


def after_feature(context, feature):
    context.browser.quit()
