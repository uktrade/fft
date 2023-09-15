from guardian.shortcuts import get_users_with_perms
from core.utils.generic_helpers import today_string
from core.utils.export_helpers import export_to_excel

from costcentre.models import CostCentre


def export_cost_centre_user_iterator(queryset):
    yield [
        "Cost Centre",
        "First Name",  # /PS-IGNORE
        "Last Name",  # /PS-IGNORE
    ]
    for cost_centre in queryset:
        users = get_users_with_perms(cost_centre, attach_perms=True)
        for user in users:
            yield [
                cost_centre.cost_centre_code,
                user.first_name,
                user.last_name,
            ]


def export_cost_centres(request):
    title = f"cost_centre_users_{today_string()}"
    return export_to_excel(
        CostCentre.objects.filter(active=True), export_cost_centre_user_iterator, title
    )
