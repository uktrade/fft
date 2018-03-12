from django.contrib import admin
from django.http import HttpResponse
import csv

from .models import DepartmentalGroup, Directorate
from .models import CostCentre
from .models import Analysis1
from .models import Analysis2
from .models import NaturalCode
from .models import Programme
from .models import ADIReport
from .models import Budgets
from .models import Grades
from .models import SalaryMonthlyAverage
from .models import VacanciesHeadCount
from .models import PayModelCosts
from .models import PayModel
from .models import PayCostHeadCount
from .models import AdminPayModel
from .models import GiftsAndHospitality
from .models import HotelAndTravel
from .models import SubSegments
from .models import SubSegmentUKTIMapping

from django.utils.encoding import smart_str
import openpyxl
from openpyxl.utils import get_column_letter


#  https://djangotricks.blogspot.co.uk/2013/12/how-to-export-data-as-excel.html
def export_cc_csv(modeladmin, request, queryset):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=costCentre.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u'Cost Centre'),
        smart_str(u'Cost Centre Description'),
        smart_str(u'Directorate Code'),
        smart_str(u'Directorate Name'),
        smart_str(u'Departmental Group Code'),
        smart_str(u'Departmental Group Name')
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.CCCode),
            smart_str(obj.CCName),
            smart_str(obj.Directorate.DirectorateCode),
            smart_str(obj.Directorate.DirectorateName),
            smart_str(obj.Directorate.GroupCode.GroupCode),
            smart_str(obj.Directorate.GroupCode.GroupName)
        ])
    return response


def export_cc1_csv(modeladmin, request, queryset):

    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=costCentre.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)

    scv = SmartExport(queryset)

    for row in scv.stream():
        writer.writerow(row)
    return response


export_cc1_csv.short_description = u"ShortExport CSV"

# writer = csv.writer(pseudo_buffer)
# response = StreamingHttpResponse(
#     (writer.writerow(row) for row in stream(headers, mydata_qs)),
#     content_type="text/csv")
# response['Content-Disposition'] = 'attachment; filename="all_kittens.csv"'
# return response

# http://blog.aeguana.com/2015/12/12/csv-export-data-for-django-model/
from django.db import models
from django.http import StreamingHttpResponse



class SmartExport:
    # return lists with the header name andthe objects from a queryset
    # it only follows one level of foreign key, while I would like to follow at lower levels
    def __init__(self, mydata_qs):
        self.data = mydata_qs
        self.model = mydata_qs.model # get the model
        self.model_fields = self.model._meta.fields + self.model._meta.many_to_many
        self.headers = [self.model._meta.get_field(field.name).verbose_name for field in self.model_fields]  # Create CSV headers. Horrible way to get the verbose name

    def get_row(self, obj):
        row = []
        for field in self.model_fields:
            if type(field) == models.ForeignKey:
                val = getattr(obj, field.name)
                if val:
                    val = smart_str(val)
            elif type(field) == models.ManyToManyField:
                # val = u', '.join([item.__unicode__() for item in getattr(obj, field.name).all()])
                val = u', '.join([smart_str(item) for item in getattr(obj, field.name).all()])
            elif field.choices:
                val = getattr(obj, 'get_%s_display'%field.name)()
            else:
                val = smart_str(getattr(obj, field.name))
            row.append(val.encode("utf-8"))
        return row

    def stream(self): # Helper function to inject headers
        if self.headers:
            yield self.headers
        for obj in self.data:
            yield self.get_row(obj)




# EXPORT_ITERATOR_HEADERS=['Cost Centre','Cost Centre2']
# def _export_iterator(queryset):
#     for obj in queryset:
#         yield(            obj.CCCode,
#             obj.CCName,
#             obj.Directorate.DirectorateCode,
#             obj.Directorate.DirectorateName,
#             obj.Directorate.GroupCode.GroupCode,
#             obj.Directorate.GroupCode.GroupName)


# def export_cc_xlsx(modeladmin, request, queryset):
#     import openpyxl
#     from openpyxl.utils import get_column_letter
#     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = 'attachment; filename=mymodel.xlsx'
#     wb = openpyxl.Workbook()
#     ws = wb.get_active_sheet()
#     ws.title = "MyModel"
#
#     row_num = 0
#
#     columns = [
#          (u'Cost Centre', 10),
#          (u'Cost Centre Description', 50),
#          (u'Directorate Code', 10),
#          (u'Directorate Name', 50),
#          (u'Departmental Group Code', 10),
#          (u'Departmental Group Name', 50)
#     ]
#
#     for col_num in range(len(columns)):
#         c = ws.cell(row=row_num + 1, column=col_num + 1)
#         c.value = columns[col_num][0]
#         # c.style.font.bold = True
#         # set column width
#         ws.column_dimensions[get_column_letter(col_num+1)].width = columns[col_num][1]
#
#     for obj in queryset:
#         row_num += 1
#         row = [
#             obj.CCCode,
#             obj.CCName,
#             obj.Directorate.DirectorateCode,
#             obj.Directorate.DirectorateName,
#             obj.Directorate.GroupCode.GroupCode,
#             obj.Directorate.GroupCode.GroupName
#         ]
#         for col_num in range(len(row)):
#             c = ws.cell(row=row_num + 1, column=col_num + 1)
#             c.value = row[col_num]
#
#     wb.save(response)
#     return response

def export_cc_xlsx(modeladmin, request, queryset):

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=mymodel.xlsx'
    wb = openpyxl.Workbook()
    ws = wb.get_active_sheet()
    ws.title = "MyModel"

    row_num = 0
    scv = SmartExport(queryset)

    for row in scv.stream():
        row_num += 1
        for col_num in range(len(row)):
            c = ws.cell(row=row_num + 1, column=col_num + 1)
            c.value = row[col_num]

    wb.save(response)
    return response


export_cc_xlsx.short_description = u"Export XLSX"


# Displays extra fields in the list of cost centres
class CostCentreAdmin(admin.ModelAdmin):
    list_display = ('CCCode', 'CCName', 'directorate_name', 'dg_name')

    def directorate_name(self, instance): # required to display the filed from a foreign key
        return instance.Directorate.DirectorateName

    def dg_name(self, instance):
        return instance.Directorate.GroupCode.GroupName

    directorate_name.admin_order_field = 'Directorate__DirectorateName'  # use __ to define a table field relationship
    dg_name.admin_order_field = 'Directorate__GroupCode__GroupName'  # use __ to define a table field relationship

    search_fields = ['CCCode']
    list_filter = ['Directorate__DirectorateName','Directorate__GroupCode__GroupName']
    readonly_fields = ['CCCode'] # don't allow to edit the code
    fields = ['CCCode', 'CCName', 'Directorate']  # required to display the read only field at the top
    actions = [export_cc1_csv, export_cc_xlsx] # new action to export to csv and xlsx


class DirectorateAdmin(admin.ModelAdmin):
    list_display = ('DirectorateName','dgroup_name')

    def dgroup_name(self, instance):
        return instance.GroupCode.GroupName

    dgroup_name.admin_order_field = 'GroupCode__GroupName' # use __ to define a table field relationship


admin.site.register(CostCentre, CostCentreAdmin)

admin.site.register(DepartmentalGroup)
admin.site.register(Directorate, DirectorateAdmin)

admin.site.register(Analysis1)
admin.site.register(Analysis2)
admin.site.register(NaturalCode)
admin.site.register(Programme)
admin.site.register(ADIReport)
admin.site.register(Budgets)
admin.site.register(Grades)
admin.site.register(SalaryMonthlyAverage)
admin.site.register(VacanciesHeadCount)
admin.site.register(PayModelCosts)
admin.site.register(PayModel)
admin.site.register(PayCostHeadCount)
admin.site.register(AdminPayModel)
admin.site.register(GiftsAndHospitality)
admin.site.register(HotelAndTravel)
admin.site.register(SubSegments)
admin.site.register(SubSegmentUKTIMapping)


#