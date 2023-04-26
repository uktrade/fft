from django.core.management.base import BaseCommand

from upload_split_file.models import (
    PaySplitCoefficient,
    UploadPaySplitCoefficient,
    SplitPayActualFigure,
    TemporaryCalculatedValues,
)


class Command(BaseCommand):
    help = "Delete split data."

    def handle(self, *args, **options):
        # Clear the split data. It is not in use yet,
        # but it could break the archive
        UploadPaySplitCoefficient.objects.all().delete()
        PaySplitCoefficient.objects.all().delete()
        SplitPayActualFigure.objects.all().delete()
        SplitPayActualFigure.objects.all().delete()
        TemporaryCalculatedValues.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Split data table cleared. "))
