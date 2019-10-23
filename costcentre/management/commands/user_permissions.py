from django.core.management.base import BaseCommand
from django.contrib.auth import (
    get_user_model,
)
from guardian.shortcuts import (
    get_objects_for_user,
)


class Command(BaseCommand):
    help = 'View cost centres associated with a given user'

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            help="User's email address",
            dest="email",
        )

    def handle(self, *args, **options):
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

        self.stdout.write(
            self.style.SUCCESS(
                "User with email '{}' has permissions on the following cost centres:".format(
                    options['email']
                )
            )
        )

        cost_centres = get_objects_for_user(
            user,
            'costcentre.change_costcentre'
        )

        for cost_centre in cost_centres:
            self.stdout.write(
                self.style.WARNING(
                    cost_centre
                )
            )
