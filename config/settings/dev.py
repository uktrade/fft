from .base import *  # noqa

CAN_ELEVATE_SSO_USER_PERMISSIONS = True

STATICFILES_DIRS = ("/app/front_end/build/static", "/app/node_modules/govuk-frontend")

SASS_PROCESSOR_INCLUDE_DIRS = [os.path.join("/node_modules")]

AUTHENTICATION_BACKENDS += [
    "authbroker_client.backends.AuthbrokerBackend",
]

ASYNC_FILE_UPLOAD = True

IGNORE_ANTI_VIRUS = True
