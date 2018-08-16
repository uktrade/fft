import django_filters

from core.filters import MyFilterSet
from .models import DepartmentalGroup, Directorate, CostCentre


class CostCentreFilter(MyFilterSet):

    class Meta:
        model = CostCentre
        fields = [
                  'directorate__group',
                  'directorate',
                  'cost_centre_code',
                  'cost_centre_name']

    @property
    def qs(self):
        cc = super(CostCentreFilter, self).qs
        return cc.filter(active=True)


