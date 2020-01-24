# from django.urls import path
#
# from .views import (
#     FilteredGiftHospitalityView,
#     GiftHospitalityOfferedDoneView,
#     GiftHospitalityOfferedView,
#     GiftHospitalityReceivedDoneView,
#     GiftHospitalityReceivedView,
#     quick_links,
# )

app_name = "gifts_hospitality"
urlpatterns = [
    # path("receive/", GiftHospitalityReceivedView.as_view(), name="gift-received"),
    # path("offer/", GiftHospitalityOfferedView.as_view(), name="gift-offered"),
    # path("search/", FilteredGiftHospitalityView.as_view(), name="gift-search"),
    # path(
    #     r"<int:gift_id>/received/",
    #     GiftHospitalityReceivedDoneView.as_view(),
    #     name="received-done",
    # ),
    # path(
    #     r"<int:gift_id>/offered/",
    #     GiftHospitalityOfferedDoneView.as_view(),
    #     name="offered-done",
    # ),
    # path(
    #     "quick-links/",
    #     quick_links,
    #     name="quick_links",
    # ),
]
