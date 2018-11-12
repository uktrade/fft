from core.admin import AdminActiveField, AdminImportExport

from django.contrib import admin
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.contenttypes.models import ContentType

from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from .importcsv import import_HR_class, import_grade_class
from .models import DITPeople, Grade


def _export_people_iterator(queryset):
    yield ['Name', 'Surname',
           'Grade', 'Cost Centre Code', 'Cost Centre Name',
           'Directorate', 'Group',
           'DG/Director/DD',
           'Business Partner', 'active']

    for obj in queryset:
        yield [obj.name,
               obj.surname,
               obj.grade.grade,
               obj.cost_centre.cost_centre_code,
               obj.cost_centre.cost_centre_name,
               obj.cost_centre.directorate.directorate_name,
               obj.cost_centre.directorate.group.group_name,
               obj.isdirector,
               obj.cost_centre]


class DIT_PeopleAdmin(AdminActiveField, AdminImportExport):
    list_display = ('surname', 'name', 'grade', 'isdirector', 'isbusinesspartner', 'active')

    # different fields editable if updating or creating the object
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['name', 'surname', 'employee_number', 'created', 'updated']
        else:
            return ['created', 'updated']

    # different fields visible if updating or creating the object
    def get_fields(self, request, obj=None):
        if obj:
            return ['name', 'surname', 'grade', 'isdirector', 'isbusinesspartner',
                    'active', 'created', 'updated']
        else:
            return ['name', 'surname', 'employee_number', 'grade',
                    'isdirector', 'isbusinesspartner', 'active']

    search_fields = ['name', 'surname']
    list_filter = ('active',
                   'isdirector',
                   'isbusinesspartner',
                   ('grade', RelatedDropdownFilter),
                   )

    def change_isdirector_flag(self, request, queryset, new_director_value):
        if new_director_value is True:
            msg = 'flag "is director" set'
        else:
            msg = 'flag "is director" cleared'
        q = queryset.filter(isdirector=not new_director_value)
        ct = ContentType.objects.get_for_model(queryset.model)  # for_model --> get_for_model
        for obj in q:
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ct.pk,
                object_id=obj.pk,
                object_repr=str(obj),
                action_flag=CHANGE,
                change_message=str(obj) + ' ' + msg)
        rows_updated = q.update(isdirector=new_director_value)
        if rows_updated == 1:
            message_bit = "1 {} was".format(queryset.model._meta.verbose_name)
        else:
            message_bit = \
                "{} {} were ".format(rows_updated, queryset.model._meta.verbose_name_plural)
        self.message_user(request, "{} successfully {}.".format(message_bit, msg))

    def make_not_director(self, request, queryset):
        self.change_isdirector_flag(request, queryset, False)

    def make_director(self, request, queryset):
        self.change_isdirector_flag(request, queryset, True)

    make_not_director.short_description = u"Remove the selected people from the Director list"
    make_director.short_description = u"Add the selected people to the Director list"
    actions = [make_not_director, make_director]

    @property
    def export_func(self):
        return _export_people_iterator

    @property
    def import_info(self):
        return import_HR_class


def _export_grade_iterator(queryset):
    yield ['Grade', 'Grade Description']

    for obj in queryset:
        yield [obj.grade,
               obj.gradedescription]


class GradeAdmin(AdminImportExport):
    list_display = ('grade', 'gradedescription')

    @property
    def export_func(self):
        return _export_grade_iterator

    @property
    def import_info(self):
        return import_grade_class


admin.site.register(DITPeople, DIT_PeopleAdmin)
admin.site.register(Grade, GradeAdmin)
# admin.site.register(SalaryMonthlyAverage)
# admin.site.register(PayModel)
# admin.site.register(AdminPayModel)
