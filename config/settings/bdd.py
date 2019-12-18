from .base import *  # noqa

CAN_ELEVATE_SSO_USER_PERMISSIONS = True

INSTALLED_APPS += ("behave_django",)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "../front_end/build/static"),
    os.path.join(BASE_DIR, "../node_modules/govuk-frontend"),
)

# for debug_toolbar, to activate it only on localhost
INTERNAL_IPS = ["127.0.0.1"]

SASS_PROCESSOR_INCLUDE_DIRS = [os.path.join("/node_modules")]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "core.middleware.ThreadLocalMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
]

SELENIUM_HOST = env("SELENIUM_HOST", default="fido")
SELENIUM_ADDRESS = env("SELENIUM_ADDRESS", default="selenium-hub")

ASYNC_FILE_UPLOAD = True

IGNORE_ANTI_VIRUS = False

USE_SELENIUM_HUB = env("USE_SELENIUM_HUB", default=True)

