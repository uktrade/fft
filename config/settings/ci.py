from .base import *  # noqa


CAN_ELEVATE_SSO_USER_PERMISSIONS = True
CAN_CREATE_TEST_USER = True

AUTHENTICATION_BACKENDS += [
    "user.backends.CustomAuthbrokerBackend",
]

ASYNC_FILE_UPLOAD = False

AXES_ENABLED = False

STORAGES["default"]["BACKEND"] = "django.core.files.storage.FileSystemStorage"
