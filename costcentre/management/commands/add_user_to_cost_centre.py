from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from guardian.shortcuts import assign_perm

from costcentre.models import CostCentre


class Command(BaseCommand):
    help = "View cost centres associated with a given user"

    def add_arguments(self, parser):
        parser.add_argument("--email", help="User's email address", dest="email")
        parser.add_argument(
            "--cost_centre_code",
            help="Cost Centre code",
            dest="cost_centre_code",
            type=int,
        )

    def handle(self, *args, **options):
        _User = get_user_model()
        user = _User.objects.filter(email=options["email"]).first()

        if user is None:
            self.stdout.write(
                self.style.ERROR(
                    "Cannot find user with email address {}".format(options["email"])
                )
            )
            return

        cost_centre = CostCentre.objects.filter(
            cost_centre_code=options["cost_centre_code"]
        ).first()

        if cost_centre is None:
            self.stdout.write(
                self.style.ERROR(
                    "Cannot find cost centre with code {}".format(
                        options["cost_centre_code"]
                    )
                )
            )
            return

        if user.has_perm("change_costcentre", cost_centre):
            self.stdout.write(
                self.style.ERROR(
                    "User already has permission to edit cost centre {}".format(
                        options["cost_centre_code"]
                    )
                )
            )
            return

        assign_perm("view_costcentre", user, cost_centre)
        assign_perm("change_costcentre", user, cost_centre)

        self.stdout.write(
            self.style.SUCCESS(
                "Permission to edit cost centre {} added".format(
                    options["cost_centre_code"]
                )
            )
        )
