from core.models import Programme

import csv


# define the column position in the csv file.

COLUMN_KEY = {
    'Code': 0,
    'Description': 1,
    'Type': 2,
}


def import_programme(csvfile):
    has_header = csv.Sniffer().has_header(csvfile.read(1024))
    csvfile.seek(0)  # Rewind.
    reader = csv.reader(csvfile)
    if has_header:
        next(reader)  # Skip header row.
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        print(row[0])
        obj, created = Programme.objects.get_or_update(
            ProgrammeCode=row[COLUMN_KEY['Code']],
            defaults={'ProgrammeDescription':row[COLUMN_KEY['Description']],
                'BudgetType': row[COLUMN_KEY['Type']]},
        )
