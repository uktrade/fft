import pytest

from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.fixture
def user(db, client):
    user = User.objects.create_user(
        username="staff.test",
        email="staff.test@example.com",
        password="password",
    )
    user.save()
    client.force_login(user)
    return user


@pytest.mark.parametrize(
    "url",
    [
        "/staff/edit-payroll/",
        "/staff/debug/",
    ],
)
def test_only_superuser_can_access(client, user, url):
    r = client.get(url)
    assert r.status_code == 403
