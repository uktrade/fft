from django.contrib import admin
from django.urls import path

from core.admin import AdminReadOnly

from downloadsupport.export_csv import (
    export_cost_centres,
    export_nac_hierarchy,
    export_travel_cost_centres,
)
from downloadsupport.models import DownloadLog


class AdminToolExport(AdminReadOnly):
    """This is an interface for downloading files in a
    predefined format, used to upload data to other application.
    To add a new download do the following:
    Add the code defining it in the model
    Add the iterator creating the download
    Add the url for it
    Add the export function to this class
    Add the url to the admintool_changelist.html"""

    change_list_template = "admin/admintool_changelist.html"
    list_display = ("download_type", "downloader", "download_time")
    list_display_links = None

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("export_travel_cc/", self.export_travel_cc),
            path("export-cc/", self.export_cc),
            path("export-nac/", self.export_nac),
        ]
        return my_urls + urls

    def export_travel_cc(self, request):
        DownloadLog.objects.create(
            downloader=request.user, download_type=DownloadLog.CC_TRAVEL
        )
        return export_travel_cost_centres()

    def export_cc(self, request):
        DownloadLog.objects.create(
            downloader=request.user, download_type=DownloadLog.CC_AT
        )
        return export_cost_centres()

    def export_nac(self, request):
        DownloadLog.objects.create(
            downloader=request.user, download_type=DownloadLog.NAC_H_AT
        )
        return export_nac_hierarchy()


admin.site.register(DownloadLog, AdminToolExport)
