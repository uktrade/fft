from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase, override_settings


class ClearCacheCommand(TestCase):
    @override_settings(
        CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
    )
    def test_cache(self):
        original_value = "12345678901234567890"
        cache_key = "long_cache_key"
        cache_invalidation_time = 7 * 24 * 60 * 60
        cache.set(cache_key, original_value, cache_invalidation_time)
        cached_value = cache.get(cache_key)
        assert cached_value == original_value

        call_command("clearcache")
        cached_value = cache.get(cache_key)
        assert cached_value is None
