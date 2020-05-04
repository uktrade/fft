from .base import *  # noqa

CAN_ELEVATE_SSO_USER_PERMISSIONS = True
CAN_CREATE_TEST_USER = True

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "front_end/build/static"),
    os.path.join(BASE_DIR, "node_modules/govuk-frontend"),
)

SASS_PROCESSOR_INCLUDE_DIRS = [os.path.join("/node_modules")]

AUTHENTICATION_BACKENDS += [
    "authbroker_client.backends.AuthbrokerBackend",
]

ASYNC_FILE_UPLOAD = False

IGNORE_ANTI_VIRUS = True
