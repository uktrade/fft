from django.urls import path

from .views import staff_debug_page, edit_payroll_page

app_name = "staff"

urlpatterns = [
    path("edit-payroll/", edit_payroll_page, name="edit_payroll"),
    path("debug/", staff_debug_page, name="debug"),
]
