from django.core.management.base import BaseCommand

from payroll.tasks import update_all_payroll_forecast


class Command(BaseCommand):
    help = "Update payroll forecast for a given year"

    def add_arguments(self, parser):
        parser.add_argument("financial_year", type=int)

    def handle(self, *args, **options):
        year = options["financial_year"]

        self.stdout.write(f"Updating all payroll forecasts for {year}")
        update_all_payroll_forecast(financial_year=year)

        self.stdout.write(self.style.SUCCESS("Done"))
