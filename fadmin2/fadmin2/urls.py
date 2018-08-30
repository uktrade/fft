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
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('core.urls')),  # default to core with no path
    path('core/', include('core.urls')),
    path('costcentre/', include('costcentre.urls')),
    path('chartofaccountDIT/', include('chartofaccountDIT.urls')),
    path('forecast/', include('forecast.urls')),
    path('admin/', admin.site.urls),
]

admin.site.site_header = "Finance Tool Admin"
admin.site.site_title = "Finance Tool Admin Portal"
admin.site.index_title = "Welcome to the Finance Tool Admin Portal"
