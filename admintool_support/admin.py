from django.contrib import admin

# Register your models here.
from django.urls import path

from core.admin import AdminreadOnly

from .exportcsv import export_cost_centres, export_nac_hierarchy

from .models import DownloadLog

class AdminToolExport(AdminreadOnly):
    change_list_template = "admin/admintool_changelist.html"
    list_display = ('download_type', 'downloader', 'download_time')
    list_display_links = None

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('export-cc/', self.export_cc),
            path('export-nac/', self.export_nac),
        ]
        return my_urls + urls

    def export_cc(self, request):
        #request.user
        DownloadLog.objects.create(downloader=request.user,
                                   download_type=DownloadLog.CC_AT)
        return export_cost_centres()

    def export_nac(self, request):
        DownloadLog.objects.create(downloader=request.user,
                                   download_type=DownloadLog.NAC_H_AT)
        return export_nac_hierarchy()


admin.site.register(DownloadLog, AdminToolExport)