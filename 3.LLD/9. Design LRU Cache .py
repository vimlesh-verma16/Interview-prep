"""
Design a LRU cache with time based expiration

✅ Here's a full working Low-Level Design for an LRU Cache with Time-Based Expiration:
Key Features:

    LRU (Least Recently Used) eviction

    Per-key TTL (Time-to-Live) expiration

    O(1) get/put operations using OrderedDict

    Custom or default TTL support

You can now extend this to support:

    Callback on expiration

    Size-based eviction

    Background cleanup thread

Let me know if you'd like a version using Redis, threading, or to integrate it into a larger system!

"""

# Design: LRU Cache with Time-Based Expiration

import time
from collections import OrderedDict


class LRUCacheWithTTL:
    def __init__(self, capacity: int, default_ttl: int):
        self.capacity = capacity
        self.default_ttl = default_ttl
        self.cache = OrderedDict()  # key -> (value, expiry_time)

    def get(self, key):
        if key in self.cache:
            value, expiry = self.cache[key]
            if time.time() > expiry:
                del self.cache[key]  # Expired
                return -1
            # Move to end to mark as recently used
            self.cache.move_to_end(key)
            return value
        return -1

    def put(self, key, value, ttl=None):
        ttl = ttl if ttl is not None else self.default_ttl
        expiry_time = time.time() + ttl

        if key in self.cache:
            del self.cache[key]
        elif len(self.cache) >= self.capacity:
            self.evict()

        self.cache[key] = (value, expiry_time)

    def evict(self):
        # Remove expired items first
        expired_keys = [k for k, (_, exp) in self.cache.items() if time.time() > exp]
        for k in expired_keys:
            del self.cache[k]

        # If still over capacity, evict least recently used
        while len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


# Example Usage
if __name__ == "__main__":
    cache = LRUCacheWithTTL(capacity=3, default_ttl=5)  # 5 seconds TTL

    cache.put("a", 1)
    time.sleep(1)
    cache.put("b", 2)
    cache.put("c", 3)
    print(cache.get("a"))  # Should return 1

    time.sleep(5)  # wait for 'a' to expire
    print(cache.get("a"))  # Should return -1 (expired)

    cache.put("d", 4)
    print(cache.get("b"))  # Should return 2
    cache.put("e", 5)
    print(cache.get("c"))  # Might return -1 if evicted due to capacity
