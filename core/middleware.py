from core.utils.generic_helpers import get_current_financial_year


class CoreRequestDataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.current_financial_year = get_current_financial_year()

        response = self.get_response(request)

        return response
