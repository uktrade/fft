
class NoCacheMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        response = self.get_response(request)
        response["Cache-Control"] = "private, no-cache, no-store, must-revalidate"  # noqa HTTP 1.1.
        response["Pragma"] = "no-cache"  # HTTP 1.0.
        response["Expires"] = "0"  # Proxies.

        return response
