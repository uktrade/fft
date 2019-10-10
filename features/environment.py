from behave import use_fixture
from core.behave_fixtures import django_test_runner, django_test_case
from selenium import webdriver
from django.conf import settings
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def before_all(context):
    use_fixture(django_test_runner, context)


def before_scenario(context, scenario):
    use_fixture(django_test_case, context)


def start_local():
    pass


def stop_local():
    pass


def before_feature(context, feature):
    context.browser = webdriver.Remote(
        command_executor='http://{}:4444/wd/hub'.format(settings.SELENIUM_ADDRESS),
        desired_capabilities=DesiredCapabilities.CHROME
    )
    context.browser.implicitly_wait(5)

    # self.firefox = webdriver.Remote(
    #     command_executor='http://selenium_hub:4444/wd/hub',
    #     desired_capabilities=DesiredCapabilities.FIREFOX
    # )
    # self.firefox.implicitly_wait(10)


def after_feature(context, feature):
    context.browser.quit()
