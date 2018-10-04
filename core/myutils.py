# Collection of useful functions and classes
import csv
import datetime


def financialyear():
    """ # Return the financial year for the current date
         The UK financial year starts in April, so Jan, Feb and Mar are part of the previous year
    """
    currentmonth = datetime.now().month
    currentyear = datetime.now().year
    if currentmonth < 4:  # the new financial year  starts in April
        currentyear = currentyear - 1  # before April, the financial year it is one year behind
    return currentyear


IMPORT_CSV_MODEL_KEY = 'model'
IMPORT_CSV_PK_NAME_KEY = 'pk_name'
IMPORT_CSV_PK_KEY = 'pk'
IMPORT_CSV_FIELDLIST_KEY = 'fieldlist'
IMPORT_CSV_IS_FK = 'isforeignkey'


def convert_to_bool_string(s):
    """The csv used for importing,  may have several different values for a boolean field.
    This routine converts them to True or False
    """
    truelist = ['y', 'yes', 'true', '1']
    if s.lower() in truelist:
        return ('True')
    else:
        return ('False')


# build the dict from the header row
def csvheadertodict(row):
    d = {k.strip(): v for v, k in enumerate(row)}  # swap key with value in the header row
    return d


#
# TODO  gives error if something not found. It means we are reading the wrong file
def addposition(d, h):
    """It substitute the header title with the column number in the dictionary
    passed to describe the imported model.
    Used recursion, because d can have a dictionary inside"""
    c = {}
    for k, v in d.items():
        if type(v) is dict:
            c[k] = addposition(v, h)
        else:
            if v in h:
                c[k] = h[v]
            else:
                c[k] = v
    return c


def get_pk_name(m):
    """Returns the name of the primary key of the model passed as argument."""
    if m._meta.pk._verbose_name is None:
        pkname = m._meta.pk.name
    else:
        pkname = m._meta.pk._verbose_name
    return pkname


def get_fk(m, pk_value):
    """Read an object to be used as foreign key in another record.
    It return a formatted message if it finds an error
    """
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


def get_fk_from_field(m, f_name, f_value):
    """Read an object to be used as foreign key in another record.
    It return a formatted message if it finds an error
    """
    msg = ''
    try:
        obj = m.objects.get(f_name=f_value)
    except m.DoesNotExist:
        msg = str(f_name) + ' "' + str(f_value) + '" does not exist'
        obj = None
    except ValueError:
        msg = str(f_name) + ' "' + str(f_value) + + '" wrong type'
        obj = None
    return obj, msg


def readcsvfromdict(d, row):
    m = d[IMPORT_CSV_MODEL_KEY]
    if IMPORT_CSV_PK_NAME_KEY in d:
        unique_name = d[IMPORT_CSV_PK_NAME_KEY]
    else:
        unique_name = m._meta.pk.name

    pk_header_name = d[IMPORT_CSV_PK_KEY]

    errormsg = ''
    # if we are only reading a foreign key (we don't want to create it!), get the value and return
    if IMPORT_CSV_IS_FK in d:
        return get_fk(m, row[pk_header_name])

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
        # import pdb;
        # pdb.set_trace()
         obj, created = m.objects.update_or_create(** {unique_name: row[pk_header_name].strip()},
                                                   defaults=defaultList)
        # obj, created = m.objects.update_or_create(field=row[pk_header_name].strip(),
        #                                           defaults=defaultList)
    except ValueError:
        obj = None
        errormsg = 'Valuerror'
    return obj, errormsg


def import_obj(csvfile, obj_key):
    reader = csv.reader(csvfile)
    header = csvheadertodict(next(reader))
    row_number = 1
    d = addposition(obj_key, header)
    for row in reader:
        row_number = row_number + 1
        obj, msg = readcsvfromdict(d, row)
        print(row_number, msg)


def get_col_from_obj_key(obj_key):
    """Takes the dictionary used to define the import, and
    return the list of the expected headers"""
    header_list = []
    if IMPORT_CSV_PK_KEY in obj_key:
        header_list.append(obj_key[IMPORT_CSV_PK_KEY])
    if IMPORT_CSV_IS_FK in obj_key:
        header_list.append(obj_key[IMPORT_CSV_IS_FK])
    if IMPORT_CSV_FIELDLIST_KEY in obj_key:
        for k, v in obj_key[IMPORT_CSV_FIELDLIST_KEY].items():
            if type(v) is dict:
                header_list = header_list + get_col_from_obj_key(v)
            else:
                header_list.append(v)
    return header_list


# used for import of lists needed to populate tables, when the primary key is created by the system
def import_list_obj(csvfile, model, fieldname):
    reader = csv.reader(csvfile)
    next(reader)  # skip the header
    for row in reader:
        obj, created = model.objects.update_or_create(**{fieldname: row[0].strip()})


class ImportInfo():
    """Use to define the function used to import from the Admin view list"""
    def __init__(self, key = {}, title = '', hlist = [],  my_import_func = None):
        self.key = key
        self.special_func = my_import_func
        if bool(key):
            self.header_list = get_col_from_obj_key(key)
        else:
            self.header_list = hlist

        if title == '':
            self.form_title = key[IMPORT_CSV_MODEL_KEY]._meta.verbose_name.title()
        else:
            self.form_title = title

    def my_import_func(self, c):
        if bool(self.key):
            return import_obj(c, self.key)
        else:
            return self.special_func(c)



