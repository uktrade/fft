import csv

from django.db import models
from django.http import HttpResponse
from django.utils.encoding import smart_str

import openpyxl


class SmartExport:
    """ return lists with the header name and the objects from a queryset
        it only follows one level of foreign key, while I would like to follow at lower levels
    """
    def __init__(self, mydata_qs):
        self.data = mydata_qs
        self.model = mydata_qs.model  # get the model
        self.model_fields = self.model._meta.fields + self.model._meta.many_to_many
        # Create  headers. Use the verbose name
        self.headers = \
            [self.model._meta.get_field(field.name).verbose_name for field in self.model_fields]

    def get_row(self, obj):
        row = []
        for field in self.model_fields:
            if type(field) == models.ForeignKey:
                val = getattr(obj, field.name)
                if val:
                    val = smart_str(val)
            elif type(field) == models.ManyToManyField:
                val = u', '.join([smart_str(item) for item in getattr(obj, field.name).all()])
            elif field.choices:
                val = getattr(obj, 'get_%s_display' % field.name)()
            else:
                val = smart_str(getattr(obj, field.name))
            row.append(val.encode("utf-8"))
        return row

    def stream(self):  # Helper function to inject headers
        if self.headers:
            yield self.headers
        for obj in self.data:
            yield self.get_row(obj)


def _generic_table_iterator(queryset):
    # Buidl the header
    mymodel = queryset.model  # get the model
    model_fields = mymodel._meta.fields + mymodel._meta.many_to_many
    # Create  headers. Use the verbose name
    headers = [mymodel._meta.get_field(field.name).verbose_name for field in model_fields]
    yield headers

    for obj in queryset:
        row = []
        for field in model_fields:
            if type(field) == models.ForeignKey:
                val = getattr(obj, field.name)
                if val:
                    val = smart_str(val)
            elif type(field) == models.ManyToManyField:
                val = u', '.join([smart_str(item) for item in getattr(obj, field.name).all()])
            elif field.choices:
                val = getattr(obj, 'get_%s_display' % field.name)()
            else:
                val = smart_str(getattr(obj, field.name))
            if val is None:
                val = ''

            row.append(val.encode("utf-8"))
        yield row


def export_to_csv(queryset, f):
    title = queryset.model._meta.verbose_name_plural.title()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + title + '.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))  # Excel needs UTF-8 to open the file
    for row in f(queryset):
        writer.writerow(row)
    return response


def generic_export_to_csv(queryset):
    return (export_to_csv(queryset, _generic_table_iterator))


EXCEL_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


def export_to_excel(queryset, f):
    title = queryset.model._meta.verbose_name_plural.title()
    resp = HttpResponse(content_type=EXCEL_TYPE)
    resp['Content-Disposition'] = 'attachment; filename=' + title + '.xlsx'
    wb = openpyxl.Workbook()
    ws = wb.get_active_sheet()
    ws.title = title
    row_num = 0
    for row in f(queryset):
        row_num += 1
        for col_num in range(len(row)):
            c = ws.cell(row=row_num + 1, column=col_num + 1)
            c.value = row[col_num]

    wb.save(resp)
    return resp


def generic_export_to_excel(queryset):
    return (export_to_excel(queryset, _generic_table_iterator))
