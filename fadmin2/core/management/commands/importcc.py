from django.core.management.base import BaseCommand, CommandError
from core.csvimport.costcentre import importcostcentres
from core.csvimport.treasurysegment import import_treasury_segments
from core.csvimport.programme import import_programme
from core.csvimport.treasuryCOA import import_treasury_COA
from core.csvimport.nac import import_NAC

import csv

IMPORT_TYPE = {
    'CostCentre': importcostcentres,
    'Segments' : import_treasury_segments,
    'COAs': import_treasury_COA,
    'Programmes': import_programme,
    'NAC':import_NAC,
}

class Command(BaseCommand):
    help = 'Import CC hierarchy from csv file'

    def add_arguments(self, parser):
        parser.add_argument('csv_path')
        parser.add_argument('type')

# pass the file path as an argument
# second argument will define the content of the file

    def handle(self, *args, **options):
        path = options.get('csv_path')
        importtype = options.get('type')
        csvfile = open(path, newline='', encoding='cp1252')  # Windows-1252 or CP-1252, used because of a back quote
        IMPORT_TYPE[importtype](csvfile)
        csvfile.close()







