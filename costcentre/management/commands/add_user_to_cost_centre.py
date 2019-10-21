from django.core.management.base import BaseCommand
from django.contrib.auth import (
    get_user_model,
)
from guardian.shortcuts import (
    get_objects_for_user,
)
from costcentre.models import CostCentre


class Command(BaseCommand):
    help = 'View cost centres associated with a given user'

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            help="User's email address",
            dest="email",
        )

    def handle(self, *args, **options):
        self.stdout.write(options['email'])

        _User = get_user_model()
        user = _User.objects.filter(
            email=options['email']
        ).first()

        if user is None:
            self.stdout.write(
                self.style.ERROR(
                    'Cannot find user with email address {}'.format(
                        options['email']
                    )
                )
            )
            return

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

