from core.models import CostCentre as cc, DepartmentalGroup as dg, Directorate as dir

import csv

# define the column position in the csv file.
# I don't know if a dictionary is the best structure to use
# I would like to define the column relative to each other, i.e. Groupname = groupcode + 1
# but I don't know how to do it
__columnKey = {'GroupCode': 3,
             'GroupName': 4,
             'DirectorateCode': 5,
             'DirectorateName': 6,
             'CCCode': 7,
             'CCName': 8}


def ImportCostCentres(path):
    csvfile = open(path, newline='', encoding='cp1252')  # Windows-1252 or CP-1252, used because of a back quote
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        # Create DG Group, Directorate and Cost centre
        objDG, created = dg.objects.get_or_create(
            GroupCode=row[__columnKey['GroupCode']],
            GroupName=row[__columnKey['GroupName']]
        )

        objdir, created = dir.objects.get_or_create(
            GroupCode=objDG,
            DirectorateCode=row[__columnKey['DirectorateCode']],
            DirectorateName=row[__columnKey['DirectorateName']]
        )
        obj, created = cc.objects.get_or_create(
            CCCode=row[__columnKey['CCCode']],
            CCName=row[__columnKey['CCName']],
            Directorate=objdir
        )
