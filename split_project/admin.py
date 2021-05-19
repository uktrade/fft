from django.contrib import admin
from core.admin import AdminReadOnly

from split_project.models import ProjectSplitCoefficient


class ProjectSplitCoefficientAdmin(AdminReadOnly):
    pass


# Register your models here.
admin.site.register(ProjectSplitCoefficient, ProjectSplitCoefficientAdmin)
