import csv

from django.http import HttpResponse
from django.utils.decorators import decorator_from_middleware
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.viewsets import ViewSet

from data_lake.hawk import HawkAuthentication, HawkResponseMiddleware


class DataLakeViewSet(ViewSet):
    authentication_classes = (HawkAuthentication,)
    permission_classes = ()

    @extend_schema(
        responses={
            (200, "text/csv"): OpenApiResponse(response=OpenApiTypes.STR),
        },
    )
    @decorator_from_middleware(HawkResponseMiddleware)
    def list(self, request):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={self.filename}.csv"
        writer = csv.writer(response, csv.excel)
        writer.writerow(self.title_list)
        self.write_data(writer)
        return response
