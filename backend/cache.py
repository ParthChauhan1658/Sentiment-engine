# backend/cache.py
"""Simple in-memory TTL cache for dashboard endpoints."""
import time


class TTLCache:
    def __init__(self):
        self._cache = {}

    def get(self, key):
        if key in self._cache:
            value, expiry = self._cache[key]
            if time.time() < expiry:
                return value
            del self._cache[key]
        return None

    def set(self, key, value, ttl=30):
        self._cache[key] = (value, time.time() + ttl)

    def invalidate(self, pattern=""):
        if not pattern:
            self._cache.clear()
        else:
            keys_to_delete = [k for k in self._cache if pattern in k]
            for k in keys_to_delete:
                del self._cache[k]


cache = TTLCache()
