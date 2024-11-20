import pytest
from django.contrib.auth import get_user_model


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
