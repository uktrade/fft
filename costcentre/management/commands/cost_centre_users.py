from django.core.management.base import BaseCommand
from guardian.shortcuts import get_users_with_perms

from costcentre.models import CostCentre


class Command(BaseCommand):
    help = 'View the users associated with a given cost centre'

    def add_arguments(self, parser):
        parser.add_argument(
            "--cost_centre_code",
            help="Cost Centre code",
            dest="cost_centre_code",
            type=int,
        )

    def handle(self, *args, **options):
        cost_centre = CostCentre.objects.filter(
            cost_centre_code=options['cost_centre_code']
        ).first()

        if cost_centre is None:
            self.stdout.write(
                self.style.ERROR(
                    'Cannot find cost centre with code {}'.format(
                        options['cost_centre_code']
                    )
                )
            )
            return

        users = get_users_with_perms(
            cost_centre,
            attach_perms=True,
        )

        self.stdout.write(
            self.style.SUCCESS(
                'Users with permission to edit cost centre {}:'.format(
                    options['cost_centre_code']
                )
            )
        )

        for user in users:
            self.stdout.write(
                self.style.WARNING(
                    user,
                )
            )
