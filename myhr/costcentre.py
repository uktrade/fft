import json
import logging

from django.db.models import Sum, Count
from django.http import HttpResponseBadRequest
from django.views.generic import TemplateView

from hr.models import HRModel
from myhr.serialisers import GroupSerializer

logger = logging.getLogger(__name__)

class CostCentreView(TemplateView):
    template_name = "myhr/list/costcentre.html"

    def class_name(self):
        return "wide-table"

    def get_all_costcentre_fte_sum_and_count(self, group_name=None):
        # Get all directorate FTE sum and count based on group name
        all_directorates = HRModel.objects.filter(group=group_name).values('cc').annotate(
            total_fte=Sum('fte'), total_count=Count('fte'))

        fte_sum_and_count = []
        for group in all_directorates:
            fte_sum_and_count.append({
                'group': group['cc'],
                'fte': group.get('total_fte', 0),
                'count': group.get('total_count', 0)
            })

        return fte_sum_and_count

    def get_groups_serialiser(self, group_name=None):
        get_all_groups_data = self.get_all_costcentre_fte_sum_and_count(group_name)
        group_serialiser = GroupSerializer(get_all_groups_data, many=True)
        return group_serialiser

    def get_context_data(self, **kwargs):
        self.title = "MyHR"
        group_name = self.request.GET.get('group_name')

        if not group_name:
            return HttpResponseBadRequest("missing 'group_name' parameter")

        group_serialiser = self.get_groups_serialiser(group_name)
        group_serialiser_data = group_serialiser.data
        group_data = json.dumps(group_serialiser_data)

        logger.info(f"cost centre data: {group_data}")

        context = super().get_context_data(**kwargs)
        context['group'] = 'MyHR'
        context['myhr_group_data'] = group_data
        return context