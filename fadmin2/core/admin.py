from django.contrib import admin


from .models import AdminInfo, EventLog


admin.site.register(AdminInfo)
admin.site.register(EventLog)
