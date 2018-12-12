from core.admin import AdminActiveField, AdminImportExport

from core.exportutils import generic_table_iterator

from django.contrib import admin

from .importcsv import import_gh_class, import_gh_company_class, \
    import_gh_classification_class, import_gh_category_class

from .models import  GiftAndHospitality, GiftAndHospitalityCompany, \
    GiftAndHospitalityCategory, GiftAndHospitalityClassification


class GiftAndHospitalityCompanyAdmin(AdminActiveField, AdminImportExport):
    list_display = ('gif_hospitality_company', 'sequence_no', 'active')
    list_editable = ('sequence_no',)
    search_fields = ['gif_hospitality_company']

    def get_readonly_fields(self, request, obj=None):
        return [ 'created', 'updated']

    @property
    def export_func(self):
        return generic_table_iterator

    @property
    def import_info(self):
        return import_gh_company_class



class GiftAndHospitalityCategoryAdmin(AdminActiveField, AdminImportExport):
    list_display = ('gif_hospitality_category', 'sequence_no', 'active')
    list_editable = ('sequence_no',)
    search_fields = ['gif_hospitality_category']

    def get_readonly_fields(self, request, obj=None):
        return [ 'created', 'updated']

    @property
    def export_func(self):
        return generic_table_iterator

    @property
    def import_info(self):
        return import_gh_category_class


class GiftAndHospitalityClassificationAdmin(AdminActiveField, AdminImportExport):
    list_display = ('gift_type', 'gif_hospitality_classification', 'sequence_no', 'active')
    list_editable = ('sequence_no',)
    search_fields = ['gift_type', 'gif_hospitality_classification']

    def get_readonly_fields(self, request, obj=None):
        return [ 'created', 'updated']

    @property
    def export_func(self):
        return generic_table_iterator

    @property
    def import_info(self):
        return import_gh_classification_class


class GiftAndHospitalityAdmin(AdminImportExport):

    list_display = ('id',
            'gift_type',
            'category',
            'classification',
            'group_name',
            'date_offered',
            'venue',
            'reason',
            'value',
            'band',
            'rep',
            'grade',
            'offer',
            'company_rep',
            'company',
            'action_taken',
            'entered_date_stamp',
            'entered_by')
    search_fields = ['id', 'rep', 'entered_by']

    list_filter = ('offer',
                   'gift_type',
                   'category',
                   'classification',
                   'company',)

    def get_fields(self, request, obj=None):
        return  ['gift_type',
            'category',
            'classification',
            'group_name',
            'date_offered',
            'venue',
            'reason',
            'value',
            'band',
            'rep',
            'grade',
            'offer',
            'company_rep',
            'company',
            'action_taken',
            'entered_by', 'entered_date_stamp']

    def get_readonly_fields(self, request, obj=None):
        return ['band', 'entered_by', 'entered_date_stamp']

    # Don't allow add
    def has_add_permission(self, request):
        return False

    @property
    def export_func(self):
        return generic_table_iterator

    @property
    def import_info(self):
        return import_gh_class




admin.site.register(GiftAndHospitality, GiftAndHospitalityAdmin)
admin.site.register(GiftAndHospitalityCompany, GiftAndHospitalityCompanyAdmin)
admin.site.register(GiftAndHospitalityCategory, GiftAndHospitalityCategoryAdmin)
admin.site.register(GiftAndHospitalityClassification,GiftAndHospitalityClassificationAdmin)

