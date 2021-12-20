from django.contrib import admin
from core.admin import AdminReadOnly

from upload_split_file.models import PaySplitCoefficient


class PaySplitCoefficientAdmin(AdminReadOnly):
    pass


# Register your models here.
admin.site.register(PaySplitCoefficient, PaySplitCoefficientAdmin)
