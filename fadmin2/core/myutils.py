# Collection of useful functions

import datetime
import csv

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