from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create test user"

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            help="Test user's email address",
            dest="email",
        )
        parser.add_argument(
            "--password",
            help="Test user's password",
            dest="password",
        )
        parser.add_argument(
            "--group",
            help="Group for user to join",
            dest="group",
        )
        parser.add_argument(
            "--is_admin",
            help="Is the user an admin?",
            dest="is_admin",
        )

    def handle(self, *args, **options):
        if settings.CAN_CREATE_TEST_USER:
            _User = get_user_model()

            is_admin = options["is_admin"]
            email = options["email"]
            group = options["group"]
            password = options["password"]

            if not email:
                email = "test@test.com"

            if not password:
                self.stdout.write(
                    self.style.ERROR(
                        "Please supply a password for this test user"
                    )
                )
                return

            user = _User.objects.filter(email=email).first()

            if user is None:
                user = _User(email=email, password=password)

            user.username = email
            user.email = email
            user.is_staff = True
            user.set_password(password)

            if is_admin:
                user.is_superuser = True

            user.save()

            if group:
                group = Group.objects.get(name=group)
                user.groups.add(group)
                user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    "Successfully created test user - {}".format(
                        user.email
                    )
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    "The setting CAN_CREATE_TEST_USER is "
                    "set to false, action not allowed"
                )
            )
