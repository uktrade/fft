from .base import *  # noqa

CAN_ELEVATE_SSO_USER_PERMISSIONS = True

INSTALLED_APPS += (
    'forecast_prototype',
    'webpack_loader',
)

STATICFILES_DIRS = (
    "/app/front_end/build/static",
    "/app/node_modules/govuk-frontend",
)

WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "BUNDLE_DIR_NAME": "build/",  # must end with slash
        "STATS_FILE": "/app/front_end/config/webpack-stats.json"  #os.path.join(BASE_DIR, "front_end", "fido", "build", "webpack-stats.json"),
    }
}

# for debug_toolbar, to activate it only on localhost
INTERNAL_IPS = ['127.0.0.1']


SASS_PROCESSOR_INCLUDE_DIRS = [
    os.path.join('/node_modules'),
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'core.middleware.ThreadLocalMiddleware',
    #'authbroker_client.middleware.ProtectAllViewsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
