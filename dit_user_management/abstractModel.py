from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class DjangoIntegrationMixin(models.Model):
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=('enables user to login to site ( not the admin site! just a website)')
    )

    is_staff = models.BooleanField(
        _('staff'),
        default=False,
        help_text=('minimum permission required to login to admin site')
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    class Meta:
        abstract = True


class FirstNameMixin(models.Model):
    first_name = models.CharField(_('first name'), max_length=254, blank=True)

    def get_first_name(self):
        return self.first_name

    class Meta:
        abstract = True


class LastNameMixin(models.Model):
    last_name = models.CharField(_('last name'), max_length=254, blank=True)

    def get_last_name(self):
        return self.last_name

    class Meta:
        abstract = True


class EmailAuthMixin(models.Model):
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    class Meta:
        abstract = True


class AbstractUser(DjangoIntegrationMixin, FirstNameMixin, LastNameMixin, EmailAuthMixin,
                   PermissionsMixin, AbstractBaseUser):
    objects = UserManager()
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def has_usable_password(self, request):
        return False

    class Meta:
        abstract = True
        verbose_name = _('user')
        verbose_name_plural = _('users')
