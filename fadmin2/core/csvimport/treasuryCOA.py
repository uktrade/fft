from core.models import L1Account, L2Account, L3Account, L4Account, L5Account

import csv


# define the column position in the csv file.

COLUMN_KEY = {
    'Accounts Code': 0,
    'Accounts Long Name': 1,
    'Account L0 Code': 2,
    'Account L0 Long Name': 3,
    'Account L1 Code': 4,
    'Account L1 Long Name': 5,
    'Account L2 Code': 6,
    'Account L2 Long Name': 7,
    'Account L3 Code': 8,
    'Account L3 Long Name': 9,
    'Account L4 Code': 10,
    'Account L4 Long Name': 11,
    'Account L5 Code': 12,
    'Account L5 Long Name': 13,
    'Account L5 Description': 14,
    'Economic Category Code': 15,
    'Economic Category Long Name': 16,
    'Economic Group Code': 17,
    'Economic Group Long Name': 18,
    'Economic Ringfence Code': 19,
    'Economic Ringfence Long Name': 20,
    'Economic Budget Code': 21,
    'PESA Economic Group Code': 22,
    'Sector Code': 23,
    'TES Code': 24,
    'ESA Code': 25,
    'ESA Long Name': 26,
    'ESA Group Code': 27,
    'ESA Group Long Name': 28,
    'PSAT Code': 29,
    'PSAT Long Name': 30,
    'National Accounts Code': 31,
    'National Accounts Long Name': 32,
    'Estimates Sub-Category Code': 33,
    'Estimates Category Code': 34,
    'Income Category Code': 35,
    'Estimates Column Code': 36,
    'Usage Code': 37,
    'Cash Indicator Code': 38
}


def import_treasury_COA(csvfile):
    has_header = csv.Sniffer().has_header(csvfile.read(1024))
    csvfile.seek(0)  # Rewind.
    reader = csv.reader(csvfile)
    if has_header:
        next(reader)  # Skip header row.
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:

        # Create DG Group, Directorate and Cost centre
        objL1, created = L1Account.objects.update_or_create(
            AccountL1Code=row[COLUMN_KEY['Account L1 Code']],
            defaults={'AccountL1LongName': row[COLUMN_KEY['Account L1 Long Name']],
                      'AccountsCode': row[COLUMN_KEY['Accounts Code']],
                      'AccountL0Code': row[COLUMN_KEY['Account L0 Code']],
                      },
        )
        objL2, created = L2Account.objects.update_or_create(
            AccountL2Code=row[COLUMN_KEY['Account L2 Code']],
            defaults={'AccountL1Code': objL1,
                       'AccountL2LongName':row[COLUMN_KEY['Account L2 Long Name']]
                      },
        )
        objL3, created = L3Account.objects.update_or_create(
            AccountL3Code=row[COLUMN_KEY['Account L3 Code']],
            defaults={'AccountL2Code': objL2,
                       'AccountL3LongName':row[COLUMN_KEY['Account L3 Long Name']]
                      },
        )
        objL4, created = L4Account.objects.update_or_create(
            AccountL4Code=row[COLUMN_KEY['Account L4 Code']],
            defaults={'AccountL3Code': objL3,
                       'AccountL4LongName':row[COLUMN_KEY['Account L4 Long Name']]
                      },
        )
        objL5, created = L5Account.objects.update_or_create(
            AccountL5Code=row[COLUMN_KEY['Account L5 Code']],
            defaults={'AccountL4Code': objL4,
                      'AccountL5LongName': row[COLUMN_KEY['Account L5 Long Name']],
                      'AccountL5Description': row[COLUMN_KEY['Account L5 Description']],
                      'EconomicBudgetCode': row[COLUMN_KEY['Economic Budget Code']],
                      'SectorCode': row[COLUMN_KEY['Sector Code']],
                      'EstimatesColumnCode': row[COLUMN_KEY['Estimates Column Code']],
                      'UsageCode': row[COLUMN_KEY['Usage Code']],
                      'CashIndicatorCode': row[COLUMN_KEY['Cash Indicator Code']],
                      },
        )
