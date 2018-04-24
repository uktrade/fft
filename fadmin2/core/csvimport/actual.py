from core.models import ADIReport, CostCentre

import csv

# define the column position in the csv file.
# it reflects the position of columns in the Orcle report used to download the actuals

__columnKey = {
            'Entity': 1,
            'Cost Centre': 2,
            'Account': 3,
            'Programme': 4,
            'Analysis 1': 5,
            'Analysis 2': 6,
            'Spare1' : 7,
            'April': 8,
            'May': 9,
            'June': 10,
            'July': 11,
            'August': 12,
            'September': 13,
            'October': 14,
            'November': 15,
            'December': 16,
            'January': 17,
            'February': 18,
            'March': 19,
            'Adj1': 20,
            'Adj2': 21,
            'Adj3': 22}

