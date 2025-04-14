from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.urls import path

from core.utils.generic_helpers import log_object_change
from user.download_user_cost_centre import download_cost_centres
from user.download_users import download_users_to_excel


User = get_user_model()


class UserAdmin(UserAdmin):
    change_list_template = "admin/export_user_changelist.html"

    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    def save_model(self, request, obj, form, change):
        for group in form.cleaned_data["groups"]:
            if group.name in [
                "Finance Administrator",
                "Gift and Hospitality Admin",
            ]:
                obj.is_staff = True
                break
        else:
            if not obj.is_superuser:
                obj.is_staff = False

        if len(form.cleaned_data["groups"]) > 0:
            log_object_change(
                request.user.id,
                f'user added to "{form.cleaned_data["groups"]}"',
                obj=obj,
            )

        super().save_model(request, obj, form, change)

    def get_exclude(self, request, obj=None):
        if request.user.is_superuser:
            return []

        return [
            "password",
        ]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []

        return [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "last_login",
            "is_superuser",
            "user_permissions",
            "is_staff",
            "date_joined",
        ]

    def get_urls(self):
        urls = super().get_urls()
        export_urls = [
            path("export-users/", download_users_to_excel),
            path("export-cc-user/", download_cost_centres),
        ]
        return export_urls + urls


admin.site.register(User, UserAdmin)
