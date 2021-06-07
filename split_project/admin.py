from django.contrib import admin
from core.admin import AdminReadOnly

from split_project.models import PaySplitCoefficient


class PaySplitCoefficientAdmin(AdminReadOnly):
    pass


# Register your models here.
admin.site.register(PaySplitCoefficient, PaySplitCoefficientAdmin)
