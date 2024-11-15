from django.db import connection


class DatabaseQueriesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        pre_query_count = len(connection.queries)

        response = self.get_response(request)

        post_query_count = len(connection.queries)
        query_count = post_query_count - pre_query_count
        print(f"Database queries {query_count}")

        return response
