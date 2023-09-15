import openpyxl

from django.http import HttpResponse
from guardian.shortcuts import get_users_with_perms
from core.utils.generic_helpers import today_string
from core.utils.export_helpers import EXC_TAB_NAME_LEN, EXCEL_TYPE

from costcentre.models import CostCentre


def export_cost_centres(request):
    title = f"cost_centre_users_{today_string()}"
    response = HttpResponse(content_type=EXCEL_TYPE)
    response["Content-Disposition"] = "attachment; filename=" + title + ".xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = title[:EXC_TAB_NAME_LEN]
    ws.append(["Cost Centre", "User last name","User first name", ])
    cost_centre_queryset = CostCentre.objects.filter(active=True)
    for cost_centre in cost_centre_queryset:
        users = get_users_with_perms(cost_centre, attach_perms=True)
        for user in users:
            ws.append([cost_centre.cost_centre_code, user.last_name, user.first_name])
    wb.save(response)
    return response