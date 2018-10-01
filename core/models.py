from django.contrib.auth.models import BaseUserManager
from .metamodels import TimeStampedModel
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin

#User Model Manager
class UserManager(BaseUserManager):

    def create_user(self,email,password=None,first_name=None,last_name=None):

        if not email:
            raise ValueError('User must have an Email Address')

        user = self.model(email=self.normalize_email(email),first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_staff_user(self,email,password,first_name,last_name):

        user = self.create_user(email,password=password,first_name=first_name,last_name=last_name)
        user.staff = True
        user.save(using=self._db)

        return user

    def create_superuser(self,email,password,first_name,last_name):

        user = self.create_user(email,password=password,first_name=first_name,last_name=last_name)
        user.staff = True
        user.superuser = True
        user.save(using=self._db)

        return user

#Custom User Model
class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True)
    first_name = models.CharField(default=None,max_length=255,blank=True)
    last_name  = models.CharField(default=None,max_length=255,blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return self.is_superuser

    def has_module_perms(self,app_label):
        return self.is_superuser

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_superuser(self):
        return self.superuser

    @property
    def is_active(self):
        return self.active

    objects = UserManager()
class AdminInfo(models.Model):
    """Used for general information for the application.
       The current month is the calendar month, 1 for jan, etc, calendar month, not financial
       Financial year is the first year of the financial year, ie 2018 for 2018-19 financial year
    """
    current_month = models.IntegerField()  #
    current_financial_year = models.IntegerField()


class EventLog(TimeStampedModel):
    EventType = models.CharField(max_length=500)
