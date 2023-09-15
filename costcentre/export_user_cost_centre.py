import csv

from django.http import HttpResponse
from guardian.shortcuts import get_users_with_perms
from core.utils.generic_helpers import today_string

from costcentre.models import CostCentre


def export_cost_centres(request):
    title = f"cost_centre_users_{today_string()}"
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=" + title + ".csv"
    writer = csv.writer(response, csv.excel)
    response.write("\ufeff".encode("utf8"))  # Excel needs UTF-8 to open the file
    writer.writerow(["Cost Centre", "User last name","User first name", ])
    cost_centre_queryset = CostCentre.objects.filter(active=True)
    for cost_centre in cost_centre_queryset:
        users = get_users_with_perms(cost_centre, attach_perms=True)
        for user in users:
            writer.writerow([cost_centre.cost_centre_code, user.last_name, user.first_name])
    return response