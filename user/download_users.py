from django.contrib.auth import get_user_model
from django.contrib.postgres.aggregates import StringAgg

from core.utils.export_helpers import export_to_excel


User = get_user_model()


def export_user_iterator(queryset):
    yield [
        "First Name",  # /PS-IGNORE
        "Last Name",  # /PS-IGNORE
        "Roles",
        "Last login",
    ]
    for obj in queryset:
        yield [
            obj["first_name"],
            obj["last_name"],
            obj["group_list"],
            obj["last_login"],
        ]


def download_users_to_excel(request):
    queryset = (
        User.objects.filter(is_active=True, groups__isnull=False)
        .annotate(group_list=StringAgg("groups__name", delimiter=", ", distinct=True))
        .values("first_name", "last_name", "group_list", "last_login")
    )
    return export_to_excel(queryset, export_user_iterator, "FFT User List")
