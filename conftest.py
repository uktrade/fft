import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def test_user(db):
    test_user_email = "test@test.com"
    test_password = "test_password"

    test_user, _ = get_user_model().objects.get_or_create(
        username="test_user",
        email=test_user_email,
    )
    test_user.set_password(test_password)
    test_user.save()

    return test_user
