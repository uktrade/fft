from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from costcentre.management.commands.directorate_permission import (
    give_access_to_directorate
)
from costcentre.models import DepartmentalGroup, Directorate


class Command(BaseCommand):
    help = "Give edit permission to all the cost centre in a given group"

    def add_arguments(self, parser):
        parser.add_argument("--email", help="User's email address", dest="email")
        parser.add_argument(
            "--group_code",
            help="Directorate code",
            dest="group_code",
            type=str,
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
        group_code = options["group_code"]
        group = DepartmentalGroup.objects.filter(
            group_code=group_code
        ).first()

        if group is None:
            self.stdout.write(
                self.style.ERROR(
                    f"Cannot find group with code {group_code}"
                )
            )
            return

        directorate_list = Directorate.objects.filter(group=group)
        group_assigned_cc = []
        group_already_assigned_cc = []

        for directorate in directorate_list:
            assigned_cc, already_assigned_cc = \
                give_access_to_directorate(directorate, user)

        if assigned_cc:
            group_assigned_cc.extend(assigned_cc)

        if already_assigned_cc:
            group_already_assigned_cc.extend(already_assigned_cc)

        if group_already_assigned_cc:
            self.stdout.write(
                self.style.ERROR(
                    f"User already has permission "
                    f"to edit cost centre {group_already_assigned_cc}"
                )
            )

        if group_assigned_cc:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Permission to edit cost centre {group_assigned_cc} added"
                )
            )
