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
            'April': 7,
            'May': 8,
            'June': 9,
            'July': 10,
            'August': 11,
            'September': 12,
            'October': 13,
            'November': 14,
            'December': 15,
            'January': 16,
            'February': 17}

