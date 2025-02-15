import factory
from django.contrib.auth import get_user_model
from faker import Faker

from core.models import FinancialYear


fake = Faker()


class FinancialYearFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FinancialYear
        django_get_or_create = ("financial_year",)

    current = True
    financial_year = 2019


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = fake.email()
    password = factory.PostGenerationMethodCall("set_password", "test_password")
