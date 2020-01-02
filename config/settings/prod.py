from .base import *  # noqa
#import environ
#
# SASS_PROCESSOR_INCLUDE_DIRS = [
#     os.path.join(env('NODE_PATH'), '/govuk-frontend/govuk/all'),
# ]

# WEBPACK_LOADER = {
#     "DEFAULT": {
#         "CACHE": not DEBUG,
#         "BUNDLE_DIR_NAME": "build/",  # must end with slash
#         "STATS_FILE": "/app/front_end/config/webpack-stats.json"  #os.path.join(BASE_DIR, "front_end", "fido", "build", "webpack-stats.json"),
#     }
# }
#env = environ.Env()

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
