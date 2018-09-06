from urllib.parse import urljoin

from django.urls import reverse
from django.shortcuts import redirect
from django.conf import settings

from requests_oauthlib import OAuth2Session


TOKEN_SESSION_KEY = '_authbroker_token'
PROFILE_URL = urljoin(settings.AUTHBROKER_URL, '/api/v1/user/me/')
INTROSPECT_URL = urljoin(settings.AUTHBROKER_URL, 'o/introspect/')
TOKEN_URL = urljoin(settings.AUTHBROKER_URL, '/o/token/')
AUTHORISATION_URL = urljoin(settings.AUTHBROKER_URL, '/o/authorize/')
TOKEN_CHECK_PERIOD_SECONDS = 60
SCOPE = 'read write'


def get_client(request, **kwargs):
    return OAuth2Session(
        settings.AUTHBROKER_CLIENT_ID,
        redirect_uri=request.build_absolute_uri(reverse('authbroker_callback')),
        scope=SCOPE,
        token=request.session.get(TOKEN_SESSION_KEY, None),
        **kwargs)


def has_valid_token(request):
    """Does the session have a valid token?"""

    return get_client(request).authorized


def authbroker_login_required(func):
    """Check that the current session has authenticated with the authbroker and has a valid token.
    This is different to the @login_required decorator in that it only checks for a valid authbroker Oauth2 token,
    not an authenticated django user."""

    def decorated(request):
        if not has_valid_token(request):
            return redirect('authbroker_login')

        return func(request)
    return decorated
