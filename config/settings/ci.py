from .base import *  # noqa


CAN_ELEVATE_SSO_USER_PERMISSIONS = True
CAN_CREATE_TEST_USER = True

AUTHENTICATION_BACKENDS += [
    "user.backends.CustomAuthbrokerBackend",
]

ASYNC_FILE_UPLOAD = False

AXES_ENABLED = False

STORAGES["default"]["BACKEND"] = "django.core.files.storage.FileSystemStorage"

# I'm not aware of any case where we need the history whilst running tests. This should
# hopefully speed up the tests a little bit.
SIMPLE_HISTORY_ENABLED = False
