import csv

from core.utils import today_string

from django.db import models
from django.http import HttpResponse
from django.utils.encoding import smart_str

import openpyxl

from .importcsv import IMPORT_CSV_MODEL_KEY, get_col_from_obj_key, get_field_name

# The max lenght for an Excel tab name is 31. So truncate the name, if needed
EXC_TAB_NAME_LEN = 31


def get_fk_value(obj, field, novalue='-'):
    if obj is not None:
        return getattr(obj, field)
    else:
        return novalue


def is_number(s):
    try:
        num = int(s)
        return num
    except ValueError:
        try:
            num = float(s)
            return num
        except ValueError:
            return s


def display_yes_no(row):
    """It takes a row generated for export and change boolean to string 'Yes' or 'No' instead of True/False"""
    for ind, item in enumerate(row):
        if isinstance(item, bool):
            if item:
                row[ind] = 'Yes'
            else:
                row[ind] = 'No'
    return row

# NOT USED
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


def generic_table_iterator(queryset):
    # Build the header
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


def export_to_csv(queryset, f, title=''):
    if title == '':
        title = queryset.model._meta.verbose_name_plural.title() + today_string()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + title + '.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))  # Excel needs UTF-8 to open the file
    for row in f(queryset):
        writer.writerow(row)
    return response


def generic_export_to_csv(queryset):
    return (export_to_csv(queryset, generic_table_iterator))


EXCEL_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


# '           application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

def export_to_excel(queryset, f, title=''):
    if title == '':
        title = queryset.model._meta.verbose_name_plural.title()
    resp = HttpResponse(content_type=EXCEL_TYPE)
    filename = title + today_string() + ' ' + '.xlsx'
    resp['Content-Disposition'] = 'attachment; filename=' + filename
    wb = openpyxl.Workbook()
    ws = wb.get_active_sheet()
    # Truncate the tab name to the maximum lenght permitted by Excel
    ws.title = title[:EXC_TAB_NAME_LEN]
    for row in f(queryset):
        # ws.append(row)
        ws.append(display_yes_no(row))
    wb.save(resp)
    return resp


def generic_export_to_excel(queryset):
    return (export_to_excel(queryset, generic_table_iterator))


class export_csv_from_import():
    def __init__(self, obj_key):
        model = obj_key[IMPORT_CSV_MODEL_KEY]
        field_list = get_field_name(obj_key, '')
        self.header_list = get_col_from_obj_key(obj_key)
        self.queryset = model.objects.all().values(*field_list)

    def yield_data(self, q):
        yield self.header_list
        for obj in q:
            yield list(obj.values())
