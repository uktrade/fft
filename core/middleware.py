try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()


def get_current_user():
    """ returns the current user's id, if a user exist, otherwise returns None """
    return getattr(_thread_locals, "user_id", None)


class ThreadLocalMiddleware:
    """ Simple middleware that adds the request object in thread local storage."""

    def __init__(self, get_response):
        self.get_response = get_response
        print("__init__")
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # Save the user into the local thread, so it can be used when saving/modifing a model

        setattr(_thread_locals, "user_id", request.user.id)
        return self.get_response(request)
