from django.contrib.auth import get_user_model
from django.test import TestCase, modify_settings, override_settings


TEST_EMAIL = "test@test.com"  # /PS-IGNORE
TEST_COST_CENTRE = 888812


@modify_settings(
    MIDDLEWARE={
        "remove": "authbroker_client.middleware.ProtectAllViewsMiddleware",
    },
    AUTHENTICATION_BACKENDS={
        "remove": "authbroker_client.backends.AuthbrokerBackend",
    },
)
@override_settings(AXES_ENABLED=False)
class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user_email = TEST_EMAIL
        cls.test_password = "test_password"

        cls.test_user, _ = get_user_model().objects.get_or_create(
            username="test_user",
            email=cls.test_user_email,
        )
        cls.test_user.set_password(cls.test_password)
        cls.test_user.save()
