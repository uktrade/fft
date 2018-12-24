from .views import DITPeopleAutocomplete
from django.conf.urls import url

urlpatterns = [
    url(
        r'^people-autocomplete/$',
        DITPeopleAutocomplete.as_view(),
        name='people-autocomplete',
    ),
]