from django.conf.urls import url

from .views import DITPeopleAutocomplete


urlpatterns = [
    url(
        r"^people-autocomplete/$",
        DITPeopleAutocomplete.as_view(),
        name="people-autocomplete",
    )
]
