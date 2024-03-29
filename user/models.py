from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    sso_contact_email = models.EmailField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return "{} - {}".format(
            self.first_name,
            self.last_name,
        )

    class Meta(AbstractUser.Meta):
        permissions = [
            ("can_download", "Can download active users"),
        ]
