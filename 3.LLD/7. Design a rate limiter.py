# ✅ What is a Rate Limiter?

# A rate limiter is a mechanism used to control how frequently a user, service, or client can access a system or resource within a specific time frame.


# 4. Common Rate Limiting Algorithms (Choose Based on Constraints)
# | Algorithm                  | Pros                                  | Cons                        | Use Case                     |
# | -------------------------- | ------------------------------------- | --------------------------- | ---------------------------- |
# | **Fixed Window**           | Simple to implement                   | Allows burst at window edge | Basic rate limiting          |
# | **Sliding Window Log**     | High accuracy                         | Memory intensive            | Low-traffic, accurate limits |
# | **Sliding Window Counter** | Less memory, more accurate than fixed | Approximate                 | APIs                         |
# | **Token Bucket**           | Smooth flow, allows bursts            | Slightly complex            | APIs with bursty traffic     |
# | **Leaky Bucket**           | Even flow of requests                 | No burst allowed            | Queue-like behavior needed   |


"""
Functional Requirements for a Rate Limiter
1. Limit Requests Per Time Window
    Example: Allow 100 requests per 60 seconds.
    Time window should be configurable (e.g., per second, minute, hour).

2. Identify Clients Uniquely
    Clients can be identified by:
        API key
        User ID
        IP address
        Session token

3. Configurable Policies per Client or Tier
    Different limits per user tier (e.g., Free, Premium).
    Different limits per endpoint (e.g., login, upload).
    Support for IP ranges or customer types.
4. Return Appropriate Response
    Allow request if under the limit.
    Return HTTP 429 (Too Many Requests) if over the limit.

5. Expose Rate Limit Metadata (Optional)
    HTTP response headers:
        X-RateLimit-Limit: Total allowed requests
        X-RateLimit-Remaining: Remaining allowed requests.
        Retry-After: Time (in seconds) until limit resets.

6. Global vs Per-User Limits
    Support:
        Per-user limits
        Per-IP limits
        Global rate limits
7. Support for Distributed Systems
    Must work across multiple service instances.
    Use shared storage (e.g., Redis, Memcached) for synchronization.
8. Bursty Traffic Handling
    Allow short bursts using algorithms like:
        Token Bucket
        Leaky Bucket
9. Sliding vs Fixed Window Support
    Support both:
        Fixed window (simpler)
        Sliding window (more fairness)
10. API Scope-Based Limiting
    Different limits for different API paths or services.
11. Admin Override Support
    Admins can:
        Update limits dynamically.
        Disable limits temporarily for a user.
12. Logging and Monitoring
    Track violations and usage metrics for analytics/debugging.

13. Notifications
    Notify users or internal systems when nearing/exceeding limits.
14. Grace Period Option
    Allow a soft limit or short grace period before strict enforcement.
15. Token Cost Customization
    Some requests can consume multiple tokens based on:
        Complexity
        Payload size
"""
# Full Implementation of a Configurable Rate Limiter (Supports Fixed/Sliding Window, Token Cost, Tiered Users)

import time
from typing import Dict, Optional
from collections import defaultdict


# ---------------------------
# Policy Definition
# ---------------------------
class Policy:
    def __init__(self, limit: int, window_seconds: int, token_cost: int = 1):
        self.limit = limit
        self.window_seconds = window_seconds
        self.token_cost = token_cost


# ---------------------------
# Client Identifier
# ---------------------------
class ClientIdentifier:
    def identify(self, request: Dict) -> str:
        return (
            request.get("api_key")
            or request.get("user_id")
            or request.get("ip")
            or request.get("session_token")
        )


# ---------------------------
# Rate Limit Policy Manager
# ---------------------------
class RateLimitPolicyManager:
    def __init__(self):
        self.tier_policies = {
            "free": {"/upload": Policy(5, 60, token_cost=2), "*": Policy(10, 60)},
            "premium": {"/upload": Policy(50, 60, token_cost=2), "*": Policy(100, 60)},
        }
        self.overrides = {}  # admin overrides

    def get_policy(self, client_id: str, endpoint: str) -> Policy:
        if client_id in self.overrides:
            return self.overrides[client_id]

        tier = "free" if client_id.startswith("free") else "premium"
        tier_policy = self.tier_policies.get(tier, {})
        return tier_policy.get(endpoint, tier_policy.get("*"))

    def set_override(self, client_id: str, policy: Policy):
        self.overrides[client_id] = policy


# ---------------------------
# Sliding Window Strategy
# ---------------------------
class SlidingWindowStrategy:
    def __init__(self):
        self.timestamps = defaultdict(list)

    def allow(self, client_id: str, policy: Policy) -> bool:
        now = time.time()
        window_start = now - policy.window_seconds
        self.timestamps[client_id] = [
            ts for ts in self.timestamps[client_id] if ts > window_start
        ]

        current_count = len(self.timestamps[client_id])
        if current_count + policy.token_cost <= policy.limit:
            self.timestamps[client_id].extend([now] * policy.token_cost)
            return True
        return False

    def get_metadata(
        self, client_id: str, policy: Policy, exceeded: bool = False
    ) -> Dict[str, str]:
        remaining = max(policy.limit - len(self.timestamps[client_id]), 0)
        headers = {
            "X-RateLimit-Limit": str(policy.limit),
            "X-RateLimit-Remaining": str(remaining),
        }
        if exceeded and self.timestamps[client_id]:
            retry_after = int(
                policy.window_seconds - (time.time() - self.timestamps[client_id][0])
            )
            headers["Retry-After"] = str(max(retry_after, 0))
        return headers


# ---------------------------
# Rate Limiter Core
# ---------------------------
class RateLimiter:
    def __init__(self, strategy, policy_manager: RateLimitPolicyManager):
        self.identifier = ClientIdentifier()
        self.strategy = strategy
        self.policy_manager = policy_manager
        self.logs = []

    def allow_request(self, request: Dict, endpoint: str):
        client_id = self.identifier.identify(request)
        policy = self.policy_manager.get_policy(client_id, endpoint)
        allowed = self.strategy.allow(client_id, policy)
        headers = self.strategy.get_metadata(client_id, policy, exceeded=not allowed)

        self.logs.append(
            {
                "client_id": client_id,
                "endpoint": endpoint,
                "allowed": allowed,
                "timestamp": time.time(),
                "headers": headers,
            }
        )

        return allowed, headers

    def get_logs(self):
        return self.logs


# ---------------------------
# Example Usage
# ---------------------------
if __name__ == "__main__":
    strategy = SlidingWindowStrategy()  # or FixedWindowStrategy()
    policy_manager = RateLimitPolicyManager()
    limiter = RateLimiter(strategy, policy_manager)

    request_example = {"api_key": "free_user_001", "ip": "192.168.1.1"}
    endpoint = "/upload"

    for i in range(8):
        allowed, headers = limiter.allow_request(request_example, endpoint)
        print(
            f"Request {i + 1}: {'Allowed' if allowed else 'Blocked'}, Headers: {headers}"
        )

    print("\nLogs:")
    for log in limiter.get_logs():
        print(log)
