from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.urls import path

from core.utils.generic_helpers import log_object_change
from costcentre.models import CostCentre
from forecast.services import get_users_cost_centres, update_users_cost_centres
from user.download_user_cost_centre import download_cost_centres
from user.download_users import download_users_to_excel


User = get_user_model()


class UserCostCentre(User):
    class Meta:
        proxy = True


class UserCostCentreForm(forms.ModelForm):
    class Meta:
        model = UserCostCentre
        fields = ["cost_centres", "groups"]
        widgets = {
            "groups": FilteredSelectMultiple("Groups", is_stacked=False),
        }

    cost_centres = forms.ModelMultipleChoiceField(
        queryset=CostCentre.objects.all(),
        required=False,
        widget=FilteredSelectMultiple("Cost centres", is_stacked=False),
    )

    def __init__(self, *args, **kwargs):
        if "initial" not in kwargs:
            kwargs["initial"] = {}
        kwargs["initial"]["cost_centres"] = get_users_cost_centres(kwargs["instance"])
        super().__init__(*args, **kwargs)


class UserCostCentreAdmin(admin.ModelAdmin):
    form = UserCostCentreForm
    fieldsets = (
        (
            "Groups",
            {
                "fields": ("groups",),
            },
        ),
        (
            "Cost centres",
            {
                "fields": ("cost_centres",),
            },
        ),
    )
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        update_users_cost_centres(obj, form.cleaned_data["cost_centres"])


class CustomUserAdmin(UserAdmin):
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


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserCostCentre, UserCostCentreAdmin)
