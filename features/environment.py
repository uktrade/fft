import datetime
import time

import pyperclip

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

from behave_django.testcase import BehaviorDrivenTestCase

from django.conf import settings
from django.contrib.auth import (
    SESSION_KEY,
    BACKEND_SESSION_KEY,
    HASH_SESSION_KEY,
)
from django.contrib.auth import get_user_model
from django.contrib.sessions.backends.db import SessionStore

from core.models import FinancialYear
from core.myutils import get_current_financial_year
from core.test.factories import FinancialYearFactory

from costcentre.test.factories import (
    CostCentreFactory,
)

from chartofaccountDIT.test.factories import (
    Analysis1Factory,
    Analysis2Factory,
    BudgetType,
    NaturalCodeFactory,
    ProgrammeCodeFactory,
    ProjectCodeFactory,
)

from forecast.models import (
    FinancialCode,
    FinancialPeriod,
    ForecastEditLock,
    ForecastMonthlyFigure,
)
from forecast.test.factories import (
    FinancialPeriodFactory,
    ForecastEditLockFactory,
)

TEST_COST_CENTRE_CODE = 888812


def set_up_test_objects(context):
    nac_codes = [111111, 999999, ]
    analysis_1_code = "1111111"
    analysis_2_code = "2222222"
    project_code_value = "3000"

    financial_year = FinancialYear.objects.first()

    if not financial_year:
        FinancialYearFactory()

    if BudgetType.objects.count() == 0:
        BudgetType.objects.create(
            budget_type_key="DEL",
            budget_type="Programme DEL",
        )
        BudgetType.objects.create(
            budget_type_key="AME",
            budget_type="Programme AME",
        )
        BudgetType.objects.create(
            budget_type_key="ADMIN",
            budget_type="Admin",
        )

    CostCentreFactory.create(
        cost_centre_code=TEST_COST_CENTRE_CODE,
    )

    programme = ProgrammeCodeFactory.create()
    project_code = ProjectCodeFactory.create(project_code=project_code_value)
    analysis_1 = Analysis1Factory.create(analysis1_code=analysis_1_code)
    analysis_2 = Analysis2Factory.create(analysis2_code=analysis_2_code)

    for nac_code in nac_codes:
        nac_code = NaturalCodeFactory.create(
            natural_account_code=nac_code,
        )
        for financial_period in range(1, 13):
            financial_month = financial_period + 3

            if financial_month > 12:
                financial_month = financial_month - 12

            month_name = (
                financial_period,
                datetime.date(
                    get_current_financial_year(),
                    financial_month, 1
                ).strftime('%B')
            )[1]

            financial_period_count = FinancialPeriod.objects.filter(
                financial_period_code=financial_period
            ).count()

            if financial_period_count == 0:
                FinancialPeriodFactory(
                    financial_period_code=financial_period,
                    period_long_name=month_name,
                    period_short_name=month_name[0:3],
                    period_calendar_code=financial_month
                )

            financial_code = FinancialCode.objects.filter(
                cost_centre_id=TEST_COST_CENTRE_CODE,
                programme=programme,
                natural_account_code=nac_code,
                analysis1_code=analysis_1,
                analysis2_code=analysis_2,
                project_code=project_code,
            ).first()

            if not financial_code:
                financial_code = FinancialCode.objects.create(
                    cost_centre_id=TEST_COST_CENTRE_CODE,
                    programme=programme,
                    natural_account_code=nac_code,
                    analysis1_code=analysis_1,
                    analysis2_code=analysis_2,
                    project_code=project_code,
                )

            ForecastMonthlyFigure.objects.create(
                financial_year_id=get_current_financial_year(),
                financial_period_id=financial_period,
                financial_code=financial_code,
                amount=0,
            )

    if ForecastEditLock.objects.count() == 0:
        ForecastEditLockFactory.create()


def create_test_user(context):
    if not hasattr(context, 'user'):
        test_user_email = "test@test.com"
        test_password = "test_password"

        test_user, _ = get_user_model().objects.get_or_create(
            email=test_user_email
        )
        test_user.is_staff = True
        test_user.is_superuser = True
        test_user.set_password(test_password)
        test_user.save()

        context.user = test_user

        client = context.test.client
        client.login(
            email=test_user_email,
            password=test_password,
        )

        # Then create the authenticated session using the new user credentials
        session = SessionStore()
        session[SESSION_KEY] = test_user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session[HASH_SESSION_KEY] = test_user.get_session_auth_hash()
        session.save()

        # Finally, create the cookie dictionary
        cookie = {
            'name': settings.SESSION_COOKIE_NAME,
            'value': session.session_key,
            'secure': False,
            'path': '/',
        }

        context.browser.get(f'{context.base_url}/admin/login/')
        context.browser.add_cookie(cookie)
        context.browser.refresh()  # need to update page for logged in user
        context.browser.get(f'{context.base_url}/')


def paste(context):
    try:
        pyperclip.paste()
        action_chains = ActionChains(context.browser)
        action_chains.key_down(Keys.SHIFT).key_down(Keys.INSERT).perform()
    except pyperclip.PyperclipException:
        first_select = context.browser.find_element_by_id("clipboard-test")
        first_select.send_keys(Keys.CONTROL, "v")

    # Wait for UI to update
    time.sleep(2)


def copy_text(context, text):
    try:
        pyperclip.copy(text.replace("\\n", "\n"))
    except pyperclip.PyperclipException:
        context.browser.execute_script(
            """function copyToClipboard() {{
            const input = document.createElement('textarea');
            document.body.appendChild(input);
            input.value = "{}";
            input.id = "clipboard-test"
            input.focus();
            input.select();
            const isSuccessful = document.execCommand('copy');
            console.log(isSuccessful);
            input.blur();
            }}
            copyToClipboard()
            """.format(text)
        )


def before_scenario(context, scenario):
    BehaviorDrivenTestCase.host = settings.SELENIUM_HOST
    set_up_test_objects(context)


def before_feature(context, feature):
    if settings.USE_SELENIUM_HUB:
        context.browser = webdriver.Remote(
            command_executor="http://{}:4444/wd/hub".format(
                settings.SELENIUM_ADDRESS
            ),
            desired_capabilities=DesiredCapabilities.CHROME,
        )
        context.browser.implicitly_wait(5)
    else:
        context.browser = webdriver.Chrome()


def after_feature(context, feature):
    context.browser.quit()
