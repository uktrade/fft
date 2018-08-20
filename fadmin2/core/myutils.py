# Collection of useful functions and classes
from django.contrib import admin

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

IMPORT_CSV_MODEL_KEY = 'model'
IMPORT_CSV_PK_KEY = 'pk'
IMPORT_CSV_FIELDLIST_KEY = 'fieldlist'
IMPORT_CSV_IS_FK = 'isforeignkey'

# it the csv used for importing, a boolean field may have several different values. This routine converts them to True or False

def convert_to_bool_string(s):
    truelist = ['y', 'yes', 'true', '1']
    if s.lower() in truelist:
        return('True')
    else:
        return('False')

# build the dict from the header row
def csvheadertodict(row):
    d = {k.strip(): v for v, k in enumerate(row)}   # swap key with value in the header row
    return d

#it substitute the header title with the column number in the dictionary passed to describe the imported model
# TODO  gives error if something not found. It means we are reading the wrong file
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

def get_pk_name(m):
    if m._meta.pk._verbose_name is None:
        pkname = m._meta.pk.name
    else:
        pkname = m._meta.pk.name
    return pkname

def get_fk(m, pk_value):
    """Read an object to be used as foreign key in another record. It return a formatted message if it finds an error"""
    msg = ''
    try:
        obj = m.objects.get(pk=pk_value)
    except m.DoesNotExist:
        msg = get_pk_name(m) + ' "' + str(pk_value) + '" does not exist'
        obj = None
    except ValueError:
        msg = get_pk_name(m) + ' "' + str(pk_value) + '" wrong type'
        obj = None
    return obj, msg


def readcsvfromdict(d, row):
    m = d[IMPORT_CSV_MODEL_KEY]
    pkname = d[IMPORT_CSV_PK_KEY]
    errormsg = ''
    # if we are only reading a foreign key (we don't want to create it!), get the value and return
    if IMPORT_CSV_IS_FK in d:
        return get_fk(m, row[pkname])

    defaultList = {}
    for k, v in d[IMPORT_CSV_FIELDLIST_KEY].items():
        if type(v) is dict:
            defaultList[k], errormsg = readcsvfromdict(v, row)
        else:
            if m._meta.get_field(k).get_internal_type() == 'BooleanField':
                # convert the value to be True or False
                defaultList[k] = convert_to_bool_string(row[v].strip())
            else:
                defaultList[k] = row[v].strip()
    try:
        obj, created = m.objects.update_or_create(pk=row[pkname].strip(),
                                   defaults=defaultList)
        print(created)
    except ValueError:
        obj = None
        msg = 'Valuerror'
    return obj, errormsg


def import_obj(csvfile, obj_key):
    reader = csv.reader(csvfile)
    l = csvheadertodict(next(reader))
    row_number = 1
    d = addposition(obj_key, l)
    for row in reader:
        row_number = row_number + 1
        obj, msg = readcsvfromdict(d, row)
        print (row_number, msg)


# used for import of lists needed to populate tables, when the primary key is created by the system
def import_list_obj(csvfile, model, fieldname):
    reader = csv.reader(csvfile)
    next(reader) # skip the header
    for row in reader:
        obj, created = model.objects.update_or_create(**{fieldname:row[0].strip()})


