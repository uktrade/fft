from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from costcentre.models import CostCentre, Directorate

from forecast.permission_shortcuts import assign_perm


def give_access_to_directorate(directorate, user):
    assigned_list = []
    already_assign_list = []
    cost_centre_list = CostCentre.objects.filter(directorate=directorate)
    for cost_centre in cost_centre_list:
        if user.has_perm("change_costcentre", cost_centre):
            already_assign_list.append(cost_centre)
        else:
            assign_perm("change_costcentre", user, cost_centre)
            assigned_list.append(cost_centre)
    return assigned_list, already_assign_list


class Command(BaseCommand):
    help = "Give edit permission to all the cost centre in a given directorate"

    def add_arguments(self, parser):
        parser.add_argument("--email", help="User's email address", dest="email")
        parser.add_argument(
            "--directorate_code",
            help="Directorate code",
            dest="directorate_code",
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
        directorate_code = options["directorate_code"]
        directorate = Directorate.objects.filter(
            directorate_code=directorate_code
        ).first()

        if directorate is None:
            self.stdout.write(
                self.style.ERROR(
                    f"Cannot find directorate with code {directorate_code}"
                )
            )

            return

        assigned_cc, already_assigned_cc = give_access_to_directorate(directorate, user)
        if already_assigned_cc:
            self.stdout.write(
                self.style.ERROR(
                    f"User already has permission "
                    f"to edit cost centre {already_assigned_cc}"
                )
            )

        if assigned_cc:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Permission to edit cost centre {assigned_cc} added"
                )
            )
