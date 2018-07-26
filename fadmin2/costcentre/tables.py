import django_tables2 as tables
from .models import CostCentre, Directorate, DepartmentalGroup
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


class DirectorateTable(tables.Table):

    class Meta:
        model = Directorate
        template_name = 'django_tables2/bootstrap.html'
        exclude = ['created', 'updated']
        sequence = ('directorate_code', '...',  'group',)
        attrs = {"class": "table-striped table-bordered"}
        empty_text = "There are no directorates matching the search criteria..."


class DepartmentalGroupTable(tables.Table):

    class Meta:
        model = DepartmentalGroup
        template_name = 'django_tables2/bootstrap.html'
        exclude = ['created', 'updated']
        sequence = ('group_code', 'group_name',)
        attrs = {"class": "table-striped table-bordered"}
        empty_text = "There are no groups matching the search criteria..."

