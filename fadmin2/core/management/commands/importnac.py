from django.core.management.base import BaseCommand, CommandError
from csvimport.costcentre import importcostcentres
import csv


class Command(BaseCommand):
    help = 'Import Natural Account Codes from csv file'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str)
        parser.add_argument('type', type=str)


# pass the file path as an argument
# second argument will define the content of the file

    def handle(self, *args, **options):
        path = '/Users/stronal/Downloads/dbfiles/CostCentre.csv' # this must be an argument!!!
        path = options.get('csv_path')
        importcostcentres(path)







