from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase


class ClearCacheCommand(TestCase):
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
