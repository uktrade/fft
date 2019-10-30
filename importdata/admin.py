from django.contrib import admin

from core.admin import AdminReadOnly

from importdata.models import AsyncImportLog


class AsyncImportLogAdmin(AdminReadOnly):
    pass


admin.site.register(AsyncImportLog, AsyncImportLogAdmin)
