import factory
from faker import Faker

from django.contrib.auth import get_user_model

from core.models import (
    Document,
    EventLog,
    FinancialYear,
)

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = fake.email()
    password = factory.PostGenerationMethodCall(
        "set_password",
        "test_password",
    )


class EventLogFactory(factory.DjangoModelFactory):
    """
    Define EventLog Factory
    """

    class Meta:
        model = EventLog


class FinancialYearFactory(factory.DjangoModelFactory):
    """
    Define FinancialYear Factory
    """

    class Meta:
        model = FinancialYear


class DocumentFactory(factory.DjangoModelFactory):
    """
    Define Document Factory
    """

    class Meta:
        model = Document
