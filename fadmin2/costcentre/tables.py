import django_tables2 as tables

from .models import CostCentre

from core.tables import FadminTable

class CostCentreTable(FadminTable):

    group_name = tables.Column(verbose_name='Group Name', accessor='directorate.group.group_name')
    directorate_name = tables.Column(verbose_name='Directorate Name', accessor='directorate.directorate_name')

    class Meta(FadminTable.Meta):
        model = CostCentre
        fields = ('group_name',
                  'directorate_name',
                  'cost_centre_code',
                  'cost_centre_name'
        )

