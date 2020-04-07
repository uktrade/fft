from django.core.management.base import BaseCommand

from end_of_month.end_of_month_actions import end_of_month_archive
from end_of_month.models import EndOfMonthStatus


class Command(BaseCommand):
    help = (
        "Archive forecast and budget for a specific period: 1 to 12 starting from April"
    )

    def add_arguments(self, parser):
        parser.add_argument("period", type=int)

    def handle(self, *args, **options):
        period_code = options["period"]
        if period_code > 15 or period_code < 1:
            self.stdout.write(self.style.ERROR("Valid Period is between 1 and 15."))
            return

        end_of_month_info = EndOfMonthStatus.objects.filter(
            archived_period__financial_period_code=period_code
        ).first()
        if end_of_month_info.archived:
            self.stdout.write(
                self.style.ERROR("The selected period has already been archived.")
            )
            return

        highest_archived = EndOfMonthStatus.objects.filter(
            archived=True, archived_period__financial_period_code=period_code
        )

        if highest_archived.count():
            self.stdout.write(
                self.style.ERROR("A later period has already been archived.")
            )
            return

        end_of_month_archive(end_of_month_info)
        self.stdout.write(
            self.style.SUCCESS(f'Period {period_code} archived.')
        )
