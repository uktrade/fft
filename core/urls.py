import time
from django.http import HttpResponse, StreamingHttpResponse
from django.urls import path

from core import views


def slow(request):
    time.sleep(35)
    return HttpResponse()


def slow_stream(request):
    def response():
        for i in range(35):
            yield i
            time.sleep(1)

    return StreamingHttpResponse(response())


urlpatterns = [
    path("", views.index, name="index"),
    path("logout", views.logout, name="logout"),
    path("accessibility", views.AccessibilityPageView.as_view(), name="accessibility"),
    path("report/budget-report", views.budget_report, name="budget_report"),
    path("slow", slow, name="slow"),
    path("slow-stream", slow_stream, name="slow-stream"),
]
