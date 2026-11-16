"""Tests for parsing Nautobot rate limiting headers."""

import unittest
from unittest.mock import Mock

from requests.structures import CaseInsensitiveDict

from pynautobot.core.rate_limit import RateLimit

NAUTOBOT_HEADERS = {
    "RateLimit-Policy": '"rest-complexity-cost";q=1000;w=60',
    "RateLimit": '"rest-complexity-cost";r=996;t=60',
    "X-Nautobot-Cost": "4",
}


class RateLimitFromHeadersTestCase(unittest.TestCase):
    """`RateLimit.from_headers` behavior."""

    def test_from_headers(self):
        cases = [
            (
                "full Nautobot header set",
                NAUTOBOT_HEADERS,
                RateLimit(policy="rest-complexity-cost", quota=1000, window=60, remaining=996, reset=60, cost=4),
            ),
            (
                "throttled response",
                {**NAUTOBOT_HEADERS, "RateLimit": '"rest-complexity-cost";r=0;t=7', "Retry-After": "7"},
                RateLimit(
                    policy="rest-complexity-cost", quota=1000, window=60, remaining=0, reset=7, cost=4, retry_after=7
                ),
            ),
            ("no rate limit headers", {"Content-Type": "application/json"}, None),
            ("Retry-After only", {"Retry-After": "30"}, RateLimit(retry_after=30)),
            ("fractional cost", {"X-Nautobot-Cost": "4.5"}, RateLimit(cost=4.5)),
            (
                "malformed values",
                {"RateLimit": "rest-complexity-cost;r=abc;t", "Retry-After": "Wed, 21 Oct 2015 07:28:00 GMT"},
                RateLimit(policy="rest-complexity-cost"),
            ),
            ("not a mapping", Mock(), None),
        ]
        for name, headers, expected in cases:
            with self.subTest(name):
                if isinstance(headers, dict):
                    headers = CaseInsensitiveDict(headers)
                self.assertEqual(RateLimit.from_headers(headers), expected)
