from guardian.shortcuts import get_users_with_perms

from core.utils.export_helpers import export_to_excel
from core.utils.generic_helpers import today_string
from costcentre.models import CostCentre


def download_cost_centre_user_iterator(queryset):
    yield [
        "Cost Centre",
        "First Name",
        "Last Name",
    ]
    for cost_centre in queryset:
        users = get_users_with_perms(
            cost_centre, only_with_perms_in=["costcentre.change_costcentre"]
        )
        for user in users:
            yield [
                cost_centre.cost_centre_code,
                user.first_name,
                user.last_name,
            ]


def download_cost_centres(request):
    title = f"cost_centre_users_{today_string()}"
    return export_to_excel(
        CostCentre.objects.filter(active=True),
        download_cost_centre_user_iterator,
        title,
    )
