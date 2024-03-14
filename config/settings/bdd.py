from .base import *  # noqa


DEBUG = False

CAN_ELEVATE_SSO_USER_PERMISSIONS = True

INSTALLED_APPS += ("behave_django",)
INSTALLED_APPS.remove("authbroker_client")

SASS_PROCESSOR_INCLUDE_DIRS = [os.path.join("/node_modules")]

SELENIUM_HOST = env("SELENIUM_HOST", default="web")
SELENIUM_ADDRESS = env("SELENIUM_ADDRESS", default="chrome")

ASYNC_FILE_UPLOAD = True

USE_SELENIUM_HUB = env("USE_SELENIUM_HUB", default=True)

AXES_ENABLED = False
