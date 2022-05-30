from django.contrib.auth import get_user_model
from django.db.models import Q

from core.utils.export_helpers import export_to_excel


User = get_user_model()


def export_user_iterator(queryset):
    yield [
        "First Name",  # /PS-IGNORE
        "Last Name",  # /PS-IGNORE
        "Last login",
    ]
    for obj in queryset:
        yield [
            obj["first_name"],
            obj["last_name"],
            obj["last_login"],
        ]


def download_users_queryset():
    # Include users with any type of permission or part of any group
    # and superusers
    return User.objects.filter(
        Q(is_active=True)
        & (
            Q(user_permissions__isnull=False)
            | Q(groups__isnull=False)
            | Q(is_superuser=True)
        )
    ).values("first_name", "last_name", "last_login")


def download_users_to_excel(request):
    return export_to_excel(
        download_users_queryset(), export_user_iterator, "FFT User List"
    )
