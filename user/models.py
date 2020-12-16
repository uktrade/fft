from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    sso_contact_email = models.EmailField(
        blank=True,
        null=True,
    )
