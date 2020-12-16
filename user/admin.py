from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from core.utils.generic_helpers import (
    log_object_change,
)


User = get_user_model()


class UserListFilter(admin.SimpleListFilter):
    title = "users"
    parameter_name = "users"
    default_value = None

    def lookups(self, request, model_admin):
        list_of_users = []
        users = User.objects.all()

        for user in self.queryset(request, users,):
            list_of_users.append((str(user.id), user.get_short_name()))

        return sorted(list_of_users, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        if request.user.groups.filter(name="Finance Administrator").exists():
            # Remove super users and fellow finance admins
            super_users = User.objects.filter(is_superuser=True)
            id_list = [user.id for user in super_users]

            # Remove administering user
            id_list.append(request.user.id)

            return queryset.exclude(
                pk__in=id_list
            ).order_by("-last_name")

        return queryset


class UserAdmin(UserAdmin):
    list_filter = (UserListFilter,)
    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'is_superuser',
    )

    def save_model(self, request, obj, form, change):
        for group in form.cleaned_data["groups"]:
            if group.name in [
                "Finance Business Partner/BSCE",
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


admin.site.register(User, UserAdmin)
