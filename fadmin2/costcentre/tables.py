import django_tables2 as tables
from .models import CostCentre
from django_tables2.utils import A


class CostCentreTable(tables.Table):
    group = tables.Column(accessor='directorate.group')

    class Meta:
        model = CostCentre
        template_name = 'django_tables2/bootstrap.html'
        exclude = ['created', 'updated','active']
        sequence = ('cost_centre_code', '...',  'group',)
        attrs = {"class": "table-striped table-bordered"}
        empty_text = "There are no cost centres matching the search criteria..."


