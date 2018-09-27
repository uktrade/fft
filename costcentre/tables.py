import django_tables2 as tables

from core.tables import FadminTable

from .models import CostCentre


class CostCentreTable(FadminTable):
    group_name = tables.Column(verbose_name='Group Name', accessor='directorate.group.group_name')
    directorate_name = tables.Column(verbose_name='Directorate Name',
                                     accessor='directorate.directorate_name')
    director_general = tables.Column(verbose_name="Director General",
                                     accessor='directorate.group.director_general')
    director = tables.Column(verbose_name="Director", accessor='directorate.director')

    class Meta(FadminTable.Meta):
        model = CostCentre
        fields = ('group_name',
                  'directorate_name',
                  'cost_centre_code',
                  'cost_centre_name',
                  'deputy_director',
                  'director',
                  'director_general',
                  'business_partner'
                  )
