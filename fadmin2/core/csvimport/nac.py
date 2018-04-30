from core.models import L5Account, NaturalCode

import csv


#
# # define the column position in the csv file.
#

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
                    NaturalAccountCode=row[c['L6']],
                    defaults={'NaturalAccountDescription': row[c['L6_NAME']],
                    'AccountL5Code': obj}
                )
            except L5Account.DoesNotExist:
                print('error at line %d: L5 code %s does exist' % (line, row[c['OSCAR L5 Mapping']]))
            # except core.models.DoesNotExist:



