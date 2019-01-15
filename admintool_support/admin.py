from django.contrib import admin

# Register your models here.
from django.urls import path

from .exportcsv import export_cost_centres, export_nac_hierarchy

from .models import DownloadLog

class AdminToolExport(admin.ModelAdmin):
    change_list_template = "admin/admintool_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('export-cc/', self.export_cc),
            path('export-nac/', self.export_nac),
        ]
        return my_urls + urls

    def export_cc(self, request):
        return export_cost_centres()

    def export_nac(self, request):
        return export_nac_hierarchy()




admin.site.register(DownloadLog, AdminToolExport)