from .base import *  # noqa
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

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
    "authbroker_client.middleware.ProtectAllViewsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "authbroker_client.backends.AuthbrokerBackend",
    "guardian.backends.ObjectPermissionBackend",
]

STATICFILES_DIRS = ("/app/front_end/build/static",)

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

IGNORE_ANTI_VIRUS = False

# HSTS (https://man.uktrade.io/docs/procedures/1st-go-live.html)
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_PRELOAD = True

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': CELERY_BROKER_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'cache_'
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': env('DJANGO_LOG_LEVEL', default='INFO'),
        },
    },
}

SENTRY_KEY = env("SENTRY_KEY", default=None)
SENTRY_PROJECT = env("SENTRY_PROJECT", default=None)

if SENTRY_KEY and SENTRY_PROJECT:
    sentry_sdk.init(
        dsn=f"https://{SENTRY_KEY}@sentry.ci.uktrade.io/{SENTRY_PROJECT}",
        integrations=[DjangoIntegration()]
    )
