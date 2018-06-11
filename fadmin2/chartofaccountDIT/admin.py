from django.contrib import admin
from .models import Analysis1, Analysis2, NaturalCode, NACDashboardGrouping, NACCategory

admin.site.register(Analysis1)
admin.site.register(Analysis2)
admin.site.register(NaturalCode)
admin.site.register(NACDashboardGrouping)
admin.site.register(NACCategory)
