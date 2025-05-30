"""fido URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def empty_favicon(request):
    return HttpResponse(status=204)


urlpatterns = [
    path("auth/", include("authbroker_client.urls", namespace="authbroker")),
    path("", include("core.urls")),  # default to core with no path
    path("core/", include("core.urls")),
    path("costcentre/", include("costcentre.urls")),
    path("chartofaccountDIT/", include("chartofaccountDIT.urls")),
    path("end_of_month/", include("end_of_month.urls")),
    path("forecast/", include("forecast.urls")),
    path("gifthospitality/", include("gifthospitality.urls")),
    path("download_file/", include("download_file.urls")),
    path("pingdom/", include("pingdom.urls")),
    path("upload/", include("upload_file.urls")),
    path("data-lake/", include("data_lake.urls")),
    path("oscar_return/", include("oscar_return.urls")),
    path("upload_split_file/", include("upload_split_file.urls")),
    path("payroll/", include("payroll.urls")),
    # API
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-schema-swagger",
    ),
    # Admin
    path("admin/", admin.site.urls),
    # TODO - split below out into develop only?
    path("favicon.ico", empty_favicon),
    path(
        "assets/<path:asset_path>",
        RedirectView.as_view(url="/static/govuk/assets/%(asset_path)s"),
    ),
]

if settings.DEBUG:
    admin.site.site_header = "Finance Forecast Tool Admin - DEBUG"
    admin.site.site_title = "Finance Forecast Tool Admin - DEBUG"
    admin.site.index_title = "Welcome to the FFT admin site - DEBUG"
else:
    admin.site.site_header = "Finance Forecast Tool Admin"
    admin.site.site_title = "Finance Forecast Tool Admin"
    admin.site.index_title = "Welcome to the FFT admin site"

if hasattr(settings, "DEBUG_TOOLBAR_CONFIG"):
    import debug_toolbar

    urlpatterns.append(
        path("__debug__/", include(debug_toolbar.urls)),
    )
