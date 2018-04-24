from core.models import L5Account, NaturalCode

import csv


#
# # define the column position in the csv file.
#
COLUMN_KEY = {
        'Total Accounts': 0,
        'L1': 1,
        'L1_NAME': 2,
        'L2': 3,
        'L2_NAME': 4,
        'L3': 5,
        'L3_NAME': 6,
        'L4': 7,
        'L4_NAME': 8,
        'L5': 9,
        'L5_NAME': 10,
        'L6': 11,
        'L6_NAME': 12,
        'DFF-Economic Budget': 13,
        'DFF-Cash Indicator': 14,
        'DFF - VAT 41': 15,
        'Enabled': 16,
        'EPM - Income Filter': 17,
        'EPM - Planning Heading Top Level': 18,
        'EPM - Fiscal Indicator': 19,
        'EPM - Economic Ringfence': 20,
        'EPM - Rollup Group': 21,
        'EPM - Planning Heading Level 2': 22,
        'OSCAR L5 Mapping': 23,
        'FAR Consolidation': 24,
        }

#/Users/stronal/Downloads/dbfiles/4.Account Codes.csv
#csvfile = open(path, newline='', encoding='cp1252')
def import_NAC(csvfile):
    has_header = csv.Sniffer().has_header(csvfile.read(1024))
    csvfile.seek(0)  # Rewind.
    reader = csv.reader(csvfile)
    if has_header:
        myd = {k: v for v, k in enumerate(next(reader))} # build the dict from the header
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        print(row[COLUMN_KEY['L6_NAME']])
        if row[COLUMN_KEY['OSCAR L5 Mapping']].isdigit():
            try:
                obj = L5Account.objects.get(AccountL5Code=row[COLUMN_KEY['OSCAR L5 Mapping']])
                objNac, created = NaturalCode.objects.update_or_create(
                    NaturalAccountCode=row[COLUMN_KEY['L6']],
                    defaults={'NaturalAccountDescription': row[COLUMN_KEY['L6_NAME']],
                    'AccountL5Code': obj}
                )
            # except core.models.DoesNotExist:



