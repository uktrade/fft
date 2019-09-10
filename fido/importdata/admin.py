from core.admin import AdminreadOnly
from django.contrib import admin

from .models import AsyncImportLog


class AsyncImportLogAdmin(AdminreadOnly):
    pass


admin.site.register(AsyncImportLog, AsyncImportLogAdmin)
