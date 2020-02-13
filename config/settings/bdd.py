from .base import *  # noqa

CAN_ELEVATE_SSO_USER_PERMISSIONS = True

INSTALLED_APPS += ("behave_django",)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "../front_end/build/static"),
    os.path.join(BASE_DIR, "../node_modules/govuk-frontend"),
)

SASS_PROCESSOR_INCLUDE_DIRS = [os.path.join("/node_modules")]

SELENIUM_HOST = env("SELENIUM_HOST", default="fido")
SELENIUM_ADDRESS = env("SELENIUM_ADDRESS", default="selenium-hub")

ASYNC_FILE_UPLOAD = True

IGNORE_ANTI_VIRUS = False

USE_SELENIUM_HUB = env("USE_SELENIUM_HUB", default=True)
