import json
import logging

from django.db.models import Sum, Count
from django.views.generic import TemplateView

from hr.models import HRModel
from myhr.serialisers import GroupSerializer

logger = logging.getLogger(__name__)

class GroupView(TemplateView):
    template_name = "myhr/list/list.html"

    def class_name(self):
        return "wide-table"

    def get_all_group_fte_sum_and_count(self):
        groups = HRModel.objects.values('group').annotate(
            fte_sum=Sum('fte'),
            fte_count=Count('fte')
        )

        fte_sum_and_count = []
        for group in groups:
            fte_sum_and_count.append({
                'group': group['group'],
                'fte': group['fte_sum'],
                'count':group['fte_count']
            })

        return fte_sum_and_count

    def get_groups_serialiser(self):
        get_all_groups_data = self.get_all_group_fte_sum_and_count()
        group_serialiser = GroupSerializer(get_all_groups_data, many=True)
        return group_serialiser

    def get_context_data(self, **kwargs):
        self.title = "MyHR"

        group_serialiser = self.get_groups_serialiser()
        group_serialiser_data = group_serialiser.data
        group_data = json.dumps(group_serialiser_data)

        logger.info(f"group data: {group_data}")

        context = super().get_context_data(**kwargs)
        context['group'] = 'MyHR'
        context['myhr_group_data'] = group_data
        context['myhr_next_view'] = 'directorate'
        return context


class ErrorView(
    TemplateView,
):
    def dispatch(self, request, *args, **kwargs):
        return 1 / 0