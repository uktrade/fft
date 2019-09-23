from pyvirtualdisplay import Display
from selenium import webdriver
import sys
from django.core.management import call_command

from selenium.webdriver.chrome.options import Options
chrome_options = Options()


def before_all(context):
    # Add test data
    # call_command('create_stub_data', 'All')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # capabilities = {
    #     'browserName': 'chrome',
    #     'chromeOptions': {
    #         'useAutomationExtension': False,
    #         'forceDevToolsScreenshot': True,
    #         'args': ['--start-maximized', '--disable-infobars']
    #     }
    # }

    display = Display(visible=0, size=(800, 600))
    display.start()

    # now Chrome will run in a virtual display.
    # you will not see the browser.
    context.driver = webdriver.Chrome(options=chrome_options)
    context.driver.get('http://www.google.com')
    print(context.driver.title, sys.stdout)


def after_all(context):
    context.driver.close()
    context.display.stop()
