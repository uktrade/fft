from core.models import CostCentre, DepartmentalGroup, Directorate

import csv

# define the column position in the csv file.

COLUMN_KEY = {
                'GroupCode': 3,
                'GroupName': 4,
                'DirectorateCode': 5,
                'DirectorateName': 6,
                'CCCode': 7,
                'CCName': 8}


def importcostcentres(path):
    csvfile = open(path, newline='', encoding='cp1252')  # Windows-1252 or CP-1252, used because of a back quote
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        # Create DG Group, Directorate and Cost centre
        objDG, created = DepartmentalGroup.objects.get_or_create(
            GroupCode=row[COLUMN_KEY['GroupCode']],
            GroupName=row[COLUMN_KEY['GroupName']]
        )
        objdir, created = Directorate.objects.get_or_create(
            GroupCode=objDG,
            DirectorateCode=row[COLUMN_KEY['DirectorateCode']],
            DirectorateName=row[COLUMN_KEY['DirectorateName']]
        )
        obj, created = CostCentre.objects.get_or_create(
            CCCode=row[COLUMN_KEY['CCCode']],
            CCName=row[COLUMN_KEY['CCName']],
            Directorate=objdir
        )
