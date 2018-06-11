# Collection of useful functions

import datetime
import csv
from django.utils.encoding import smart_str

from django.db import models


# Return the financial year for the current date
# The UK financial year starts in April, so Jan, Feb and Mar are part of the previous year
def financialyear():
    currentmonth = datetime.now().month
    currentyear = datetime.now().year
    if currentmonth < 4 : # the new financial year  starts in April
        currentyear = currentyear - 1 # before April, the financial year it is one year behind
    return currentyear


def csvheadertodict(row):
    d = {k: v for v, k in enumerate(row)}  # build the dict from the header row
    return d


def addposition(d, h):
    c = {}
    for k,v in d.items():
        if type(v) is dict:
            c[k] = addposition(v, h)
        else:
            if v in h:
                c[k] = h[v]
            else:
                c[k] = v
    return c


def readcsvfromdict(d, row):
    m= d['model']
    pk1= d['PK']
    pkname=pk1.field_name
    exc = ['model', 'PK', pkname]
    defaultList = {}
    for k, v in d.items():
        if k not in exc:
            if type(v) is dict:
                defaultList[k] = readcsvfromdict(v, row)
            else:
                defaultList[k] = row[v]
    obj, created = m.objects.update_or_create(pk=row[d[pkname]],
                                   defaults =defaultList)
    return obj


def import_obj(csvfile, obj_key):
    # has_header = csv.Sniffer().has_header(csvfile.read(1024))
    # csvfile.seek(0)  # Rewind.
    reader = csv.reader(csvfile)
    line = 1
    l = csvheadertodict(next(reader))
#    print(l)
    d = addposition(obj_key, l)

    for row in reader:
        readcsvfromdict(d, row)



class SmartExport:
    # return lists with the header name and the objects from a queryset
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


