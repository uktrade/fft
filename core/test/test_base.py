from django.contrib.auth import get_user_model
from django.test import RequestFactory


# Nb. we're using RequestFactory here
# because SSO does not fully support
# the test client's user object
class RequestFactoryBase:
    def __init__(self):
        self.factory = RequestFactory()

        self.test_user_email = "test@test.com"
        self.test_password = "test_password"

        self.test_user, _ = get_user_model().objects.get_or_create(
            email=self.test_user_email
        )
        self.test_user.set_password(self.test_password)
        self.test_user.save()

    def factory_get(self, url, view_class, *args, **kwargs):
        # Bust permissions cache (refresh_from_db does not work)
        self.test_user, _ = get_user_model().objects.get_or_create(
            email="test@test.com"
        )

        request = self.factory.get(url)
        request.user = self.test_user
        return view_class.as_view()(request, **kwargs)

    def factory_post(self, url, post_content, view_class, *args, **kwargs):
        # Bust permissions cache (refresh_from_db does not work)
        self.test_user, _ = get_user_model().objects.get_or_create(
            email="test@test.com"
        )

        request = self.factory.post(
            url,
            post_content,
        )
        request.user = self.test_user
        return view_class.as_view()(request, **kwargs)
