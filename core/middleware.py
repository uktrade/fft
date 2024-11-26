from contextvars import ContextVar
from pprint import pprint

import sentry_sdk
from django.db import connection


class DatabaseQueriesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        pre_query_count = len(connection.queries)

        response = self.get_response(request)

        post_query_count = len(connection.queries)
        query_count = post_query_count - pre_query_count
        pprint(connection.queries)
        print(f"Database queries {query_count}")

        # https://docs.sentry.io/platforms/python/performance/instrumentation/custom-instrumentation/#accessing-the-current-transaction
        transaction = sentry_sdk.Hub.current.scope.transaction

        if transaction is not None:
            transaction.set_tag("database.query_count", query_count)

        return response


_current_financial_year = ContextVar("current_financial_year", default=None)


class CoreRequestDataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        _current_financial_year.set(None)

        return response
