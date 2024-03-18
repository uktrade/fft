from .base import *  # noqa


CAN_ELEVATE_SSO_USER_PERMISSIONS = True
CAN_CREATE_TEST_USER = True

SASS_PROCESSOR_INCLUDE_DIRS = [os.path.join("/node_modules")]

AUTHENTICATION_BACKENDS += [
    "user.backends.CustomAuthbrokerBackend",
]

ASYNC_FILE_UPLOAD = False
