from core.admin import AdminReadOnly
from django.contrib import admin

from .models import AsyncImportLog


class AsyncImportLogAdmin(AdminReadOnly):
    pass


admin.site.register(AsyncImportLog, AsyncImportLogAdmin)
