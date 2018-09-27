from django.db.models import Sum
from django.shortcuts import render

from django_tables2 import RequestConfig

from .models import ADIReport
from .tables import ADIReportTable


def adireport(request):
    table = ADIReportTable(ADIReport.objects.values('cost_centre__directorate__group__group_name')
                           .annotate(Sum('apr'), Sum('may'), Sum('jun'),
                                     Sum('jul'), Sum('aug'), Sum('sep'),
                                     Sum('oct'), Sum('nov'), Sum('dec'),
                                     Sum('jan'), Sum('feb'), Sum('mar')))
    RequestConfig(request).configure(table)
    return render(request, 'forecast/forecast.html', {'table': table})
