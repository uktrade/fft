from django.core.management.base import BaseCommand, CommandError
from csvimport.costcentre import ImportCostCentres
import csv


class Command(BaseCommand):
    help = 'Import CC hierarchy from csv file'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)


# pass the file path as an argument
# second argument will define the content of the file

    def handle(self, *args, **options):
        path = '/Users/stronal/Downloads/CostCentre.csv' # this must be an argument!!!
        ImportCostCentres(path)







