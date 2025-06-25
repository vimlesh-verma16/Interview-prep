# ✅ Functional Requirements

# 1. Shorten URL
#    - Input: Long URL (e.g., https://example.com/long/path)
#    - Output: Shortened URL (e.g., bit.ly/abc123)

# 2. Redirect
#    - Input: Short URL
#    - Output: Redirect to original long URL (HTTP 301/302)

# 3. Custom Alias (Optional)
#    - Allow custom slugs (e.g., bit.ly/myoffer)

# 4. Expiration
#    - Set expiry date/time for short URLs

# 5. Analytics (Optional)
#    - Track: Click count, Timestamp, IP, Browser/Device

# 6. Rate Limiting (Optional)
#    - Limit: 100 requests/minute per IP

import time
import threading
import string
import random
from typing import Optional
from hashlib import md5


class URL:
    def __init__(
        self, long_url: str, short_code: str, created_at=None, expires_at=None
    ):
        self.long_url = long_url
        self.short_code = short_code
        self.created_at = created_at or time.time()
        self.expires_at = expires_at
        self.click_count = 0

    def is_expired(self):
        return self.expires_at is not None and time.time() > self.expires_at

    def record_click(self):
        self.click_count += 1


class Base62Encoder:
    characters = string.ascii_letters + string.digits

    @staticmethod
    def encode(num: int) -> str:
        if num == 0:
            return Base62Encoder.characters[0]

        base = len(Base62Encoder.characters)
        result = []

        while num > 0:
            result.append(Base62Encoder.characters[num % base])
            num //= base

        return "".join(reversed(result))

    @staticmethod
    def generate_random_code(length=6) -> str:
        return "".join(random.choices(Base62Encoder.characters, k=length))


class URLRepository:
    def __init__(self):
        self.lock = threading.Lock()
        self.counter = 0
        self.short_to_url = {}
        self.long_to_short = {}

    def get_next_id(self) -> int:
        with self.lock:
            self.counter += 1
            return self.counter

    def save(self, url_obj: URL):
        self.short_to_url[url_obj.short_code] = url_obj
        self.long_to_short[url_obj.long_url] = url_obj.short_code

    def get_by_short(self, short_code: str) -> Optional[URL]:
        return self.short_to_url.get(short_code)

    def get_by_long(self, long_url: str) -> Optional[str]:
        return self.long_to_short.get(long_url)


class URLShortenerService:
    def __init__(self, repository: URLRepository):
        self.repo = repository

    def shorten_url(
        self,
        long_url: str,
        custom_alias: Optional[str] = None,
        expiry_seconds: Optional[int] = None,
    ) -> str:
        existing = self.repo.get_by_long(long_url)
        if existing:
            return existing

        short_code = custom_alias or Base62Encoder.encode(self.repo.get_next_id())

        if short_code in self.repo.short_to_url:
            raise Exception("Alias already taken")

        expires_at = time.time() + expiry_seconds if expiry_seconds else None
        url_obj = URL(long_url, short_code, expires_at=expires_at)

        self.repo.save(url_obj)
        return short_code

    def get_original_url(self, short_code: str) -> Optional[str]:
        url_obj = self.repo.get_by_short(short_code)
        if not url_obj:
            return None

        if url_obj.is_expired():
            return None

        url_obj.record_click()
        return url_obj.long_url


class AnalyticsService:
    def __init__(self, repository: URLRepository):
        self.repo = repository

    def get_click_count(self, short_code: str) -> int:
        url_obj = self.repo.get_by_short(short_code)
        if url_obj:
            return url_obj.click_count
        return 0


if __name__ == "__main__":
    repo = URLRepository()
    shortener = URLShortenerService(repo)
    analytics = AnalyticsService(repo)

    long_url = "https://www.example.com/some/very/long/path"

    short = shortener.shorten_url(long_url)
    print("Short URL:", short)

    original = shortener.get_original_url(short)
    print("Redirect to:", original)

    print("Click count:", analytics.get_click_count(short))
