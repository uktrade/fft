from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from config.perms import GROUPS


class Command(BaseCommand):
    help = "Manage the auth groups"

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        self.log(f"verbosity: {options["verbosity"]}")
        self.log(f"dry-run: {options["dry_run"]}")

        for group_name, perms in GROUPS:
            try:
                group = Group.objects.get(name=group_name)
            except Group.DoesNotExist:
                if not options["dry_run"]:
                    Group.objects.create(name=group_name)

                self.log(f"{group_name!r} created")
            else:
                if options["verbosity"] > 1:
                    self.log(f"{group_name!r} already exists")

            for perm_dot_path in perms:
                perm_app_label, perm_codename = perm_dot_path.split(".")
                perm = Permission.objects.get(
                    content_type__app_label=perm_app_label,
                    codename=perm_codename,
                )

                if group.permissions.contains(perm):
                    if options["verbosity"] > 1:
                        self.log(f"    {perm_dot_path!r} already exists")
                else:
                    if not options["dry_run"]:
                        group.permissions.add(perm)

                    if options["verbosity"] > 1:
                        self.log(f"    {perm_dot_path!r} added")

    def log(self, msg):
        self.stdout.write(msg)
