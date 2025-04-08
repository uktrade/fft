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

# Dummy cache needed to get around waffle race condition when running under xdist.
# https://github.com/jazzband/django-waffle/issues/350
CACHES["dummy_cache"] = {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}
WAFFLE_CACHE_NAME = "dummy_cache"
