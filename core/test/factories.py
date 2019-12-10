from django.contrib.auth import get_user_model

import factory

from faker import Faker

from core.models import Document, EventLog

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = fake.email()
    password = factory.PostGenerationMethodCall("set_password", "test_password")


class EventLogFactory(factory.DjangoModelFactory):
    """
    Define EventLog Factory
    """

    class Meta:
        model = EventLog


class DocumentFactory(factory.DjangoModelFactory):
    """
    Define Document Factory
    """

    class Meta:
        model = Document
