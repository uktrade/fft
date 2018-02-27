from django.core.management.base import BaseCommand, CommandError
from core.models import CostCentre as CC
import csv


class Command(BaseCommand):
    help = 'Import CC hierarchy from csv file'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)


# pass the file path as an argument
# second argument will define the content of the file

    def handle(self, *args, **options):
        # self.stdout.write("Hello, my first command!!")
        path = '/Users/stronal/Downloads/CostCentre.csv'
        csvfile = open(path, newline='', encoding='cp1252')
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvreader:
            self.stdout.write(row[2])
            # self.stdout.write(', '.join(row))
        # for poll_id in options['poll_id']:
        #     try:
        #         poll = CC.objects.get(pk=poll_id)
        #     except CC.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)
        #
        #     poll.opened = False
        #     poll.save()
        #
        #     self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
