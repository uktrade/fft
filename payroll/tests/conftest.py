import pytest
from django.conf import settings
from django.contrib.auth import get_user_model

from chartofaccountDIT.test.factories import NaturalCodeFactory


User = get_user_model()


@pytest.fixture
def user(db, client):
    user = User.objects.create_user(
        username="test",
        email="test@example.com",
        password="password",
    )
    user.save()
    client.force_login(user)
    return user


@pytest.fixture
def payroll_nacs(db):
    return [
        NaturalCodeFactory(natural_account_code=settings.PAYROLL_BASIC_PAY_NAC),
        NaturalCodeFactory(natural_account_code=settings.PAYROLL_PENSION_NAC),
        NaturalCodeFactory(natural_account_code=settings.PAYROLL_ERNIC_NAC),
    ]
