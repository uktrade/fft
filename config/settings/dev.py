from .paas import *  # noqa


MIDDLEWARE += [
    "authbroker_client.middleware.ProtectAllViewsMiddleware",
    # TODO: Move to base settings when running on all envs.
    "csp.middleware.CSPMiddleware",
]

AUTHENTICATION_BACKENDS += [
    "user.backends.CustomAuthbrokerBackend",
]

# X_ROBOTS_TAG (https://man.uktrade.io/docs/procedures/1st-go-live.html)
X_ROBOTS_TAG = [
    "noindex",
    "nofollow",
]

# Django staff SSO user migration process requries the following
MIGRATE_EMAIL_USER_ON_LOGIN = True

# Set async file uploading
ASYNC_FILE_UPLOAD = True

# HSTS (https://man.uktrade.io/docs/procedures/1st-go-live.html)
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# ## IHTC compliance

# Set crsf cookie to be secure
CSRF_COOKIE_SECURE = True

# Set session cookie to be secure
SESSION_COOKIE_SECURE = True

# Make browser end session when user closes browser
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Set cookie expiry to 4 hours
SESSION_COOKIE_AGE = 4 * 60 * 60  # 4 hours in seconds

# Prevent client side JS from accessing CRSF token
CSRF_COOKIE_HTTPONLY = True

# Prevent client side JS from accessing session cookie (true by default)
SESSION_COOKIE_HTTPONLY = True

# Set content to no sniff
SECURE_CONTENT_TYPE_NOSNIFF = True

# Set anti XSS header
SECURE_BROWSER_XSS_FILTER = True

AXES_ENABLED = False
