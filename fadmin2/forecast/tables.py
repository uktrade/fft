import django_tables2 as tables
from django_tables2.utils import A

from .models import ADIReport

#q = q = ADIReport.objects.values('cost_centre__directorate__group__group_name').annotate(Sum('apr'),Sum('may'),Sum('jun')


class ADIReportTable(tables.Table):

    class Meta:
        model = ADIReport
        fields = ('cost_centre__directorate__group__group_name', 'apr__sum','may__sum', 'jun__sum',
                  'jul__sum','aug__sum','sep__sum','oct__sum','nov__sum','dec__sum','jan__sum','feb__sum','mar__sum')
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "table-striped table-bordered"}
        empty_text = "There are no NAC matching the search criteria..."


