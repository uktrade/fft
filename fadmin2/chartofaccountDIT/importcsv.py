from .models import Analysis1, Analysis2
from core.myutils import import_obj, IMPORT_CSV_MODEL_KEY, IMPORT_CSV_PK_KEY, IMPORT_CSV_FIELDLIST_KEY



# define the column position in the csv file.

ANALYSIS1_KEY = {IMPORT_CSV_MODEL_KEY: Analysis1,
                 IMPORT_CSV_PK_KEY: 'Code',
                 IMPORT_CSV_FIELDLIST_KEY: {Analysis1.analysis1_description.field_name: 'Description'}}

ANALYSIS2_KEY = {IMPORT_CSV_MODEL_KEY: Analysis2,
                 IMPORT_CSV_PK_KEY: 'Code',
                 IMPORT_CSV_FIELDLIST_KEY: {Analysis2.analysis2_description.field_name: 'Description'}}


def import_Analysis1(csvfile):
    import_obj(csvfile, ANALYSIS1_KEY)

def import_Analysis2(csvfile):
    import_obj(csvfile, ANALYSIS2_KEY)


FIELD_LIST = ['L6', 'L6_NAME', 'OSCAR L5 Mapping' ]


#/Users/stronal/Downloads/dbfiles/4.Account Codes.csv
#csvfile = open(path, newline='', encoding='cp1252')

def import_NAC(csvfile):
    has_header = csv.Sniffer().has_header(csvfile.read(1024))
    csvfile.seek(0)  # Rewind.
    reader = csv.reader(csvfile)
    line = 1
    if has_header:
        h = {k: v for v, k in enumerate(next(reader))} # build the dict from the header
        c = {}
        for x in FIELD_LIST:
            c[x] = h[x]
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        line += 1
        if row[c['OSCAR L5 Mapping']].isdigit():
            try:
                obj = L5Account.objects.get(AccountL5Code=row[c['OSCAR L5 Mapping']])
                objNac, created = NaturalCode.objects.update_or_create(
                    natural_account_code=row[c['L6']],
                    defaults={'NaturalAccountDescription': row[c['L6_NAME']],
                    'AccountL5Code': obj}
                )
            except L5Account.DoesNotExist:
                print('error at line %d: L5 code %s does exist' % (line, row[c['OSCAR L5 Mapping']]))
            # except core.models.DoesNotExist:

