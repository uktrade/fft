"""fadmin2 URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('auth/', include('authbroker_client.urls', namespace='authbroker')),
    path('', include('core.urls')),  # default to core with no path
    path('core/', include('core.urls')),
    path('costcentre/', include('costcentre.urls')),
    path('chartofaccountDIT/', include('chartofaccountDIT.urls')),
    path('forecast/', include('forecast.urls')),
    path('gifthospitality/', include('gifthospitality.urls')),
    path('payroll/', include('payroll.urls')),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls))
    ] + urlpatterns

if settings.DEBUG:
    admin.site.site_header = "FIDO Admin - TEST"
    admin.site.site_title = "FIDO Admin Portal - TEST"
    admin.site.index_title = "Welcome to FIDO Admin Portal - TEST"
else:
    admin.site.site_header = "FIDO Admin"
    admin.site.site_title = "FIDO Admin Portal"
    admin.site.index_title = "Welcome to FIDO Admin Portal"

