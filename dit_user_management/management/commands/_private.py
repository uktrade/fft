from django.core.management.base import BaseCommand


class AbstractCommand(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("This command is disabled"))

    class Meta:
        abstract = True
