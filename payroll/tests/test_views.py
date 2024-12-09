import pytest


@pytest.mark.parametrize(
    "url",
    [
        "/payroll/edit/888812/2024/",
    ],
)
def test_only_superuser_can_access(client, user, url):
    r = client.get(url)
    assert r.status_code == 403
