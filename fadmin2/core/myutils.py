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

IMPORT_CSV_MODEL_KEY = 'model'
IMPORT_CSV_PK_KEY = 'pk'
IMPORT_CSV_FIELDLIST_KEY = 'fieldlist'

# it the csv used for importing, a boolean field may have several different values. This routine converts them to True or False

def convert_to_bool_string(s):
    truelist = ['y', 'yes', 'true', '1']
    if s.lower() in truelist:
        return('True')
    else:
        return('False')

# build the dict from the header row
def csvheadertodict(row):
    d = {k: v for v, k in enumerate(row)}   # swap key with value in the header row
    return d

#it substitute the header title with the column number in the dictionary passed to describe the imported model
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
    m = d[IMPORT_CSV_MODEL_KEY]
    pkname = d[IMPORT_CSV_PK_KEY]
    defaultList = {}
    errormsg = ''
    for k, v in d[IMPORT_CSV_FIELDLIST_KEY].items():
        if type(v) is dict:
            defaultList[k], errormsg = readcsvfromdict(v, row)
        else:
            if m._meta.get_field(k).get_internal_type() == 'BooleanField':
                # convert the value to be True or False
                defaultList[k] = convert_to_bool_string(row[v].strip())
            else:
                defaultList[k] = row[v].strip()
    # todo add a new key 'don't create, to force to give an error if the record does not exist
    # required for uploading actuals, and check the validity of Cost Centre, etc
    # use new type of record 'getkey'
    obj, created = m.objects.update_or_create(pk=row[pkname],
                                   defaults=defaultList)
    return obj, errormsg


def import_obj(csvfile, obj_key):
    reader = csv.reader(csvfile)
    l = csvheadertodict(next(reader))
    d = addposition(obj_key, l)
    for row in reader:
        readcsvfromdict(d, row)




