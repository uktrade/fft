from .base import *  # noqa


DEBUG = False

CAN_ELEVATE_SSO_USER_PERMISSIONS = True

INSTALLED_APPS += ("behave_django",)
INSTALLED_APPS.remove("authbroker_client")

# The bdd tests are run with behave-django which uses StaticLiveServerTestCase. WhiteNoise
STORAGES["staticfiles"] = {
    # "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
}

SELENIUM_HOST = env("SELENIUM_HOST", default="web")
SELENIUM_ADDRESS = env("SELENIUM_ADDRESS", default="chrome")

ASYNC_FILE_UPLOAD = True

AXES_ENABLED = False

VITE_DEV = False
