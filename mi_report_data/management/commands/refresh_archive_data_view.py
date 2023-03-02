from django.core.management.base import BaseCommand

from mi_report_data.utils import refresh_materialised_views


class Command(BaseCommand):

    help = (
        "Refresh the materialized views used to export current year archived data"
        "to data workspace"
    )

    def handle(self, *args, **options):
        refresh_materialised_views()
