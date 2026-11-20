"""Tests for retry and rate limiting behavior against a local stub Nautobot server.

A real socket is used so that requests goes through urllib3's `Retry` handling,
which mocking libraries such as `requests-mock` bypass.
"""

import json
import threading
import unittest
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

import pynautobot
from pynautobot.core.query import RequestErrorFromException

TOKEN = "0123456789abcdef0123456789abcdef01234567"
POLICY = '"rest-complexity-cost";q=1000;w=60'
THROTTLED = (
    429,
    {
        "Retry-After": "7",
        "RateLimit": '"rest-complexity-cost";r=0;t=7',
        "RateLimit-Policy": POLICY,
        "X-Nautobot-Cost": "3",
    },
    {"detail": "Request was throttled. The estimated complexity cost exceeds the budget."},
)
DEVICE = {"id": "db8770c4-61e5-4999-8372-e7fa576a4f65", "name": "dev1"}
DEVICE_LIST = {"count": 1, "next": None, "previous": None, "results": [DEVICE]}


def ok(body, remaining=None, status=200):
    """Build a successful scripted response, with rate limit headers when `remaining` is given."""
    headers = {}
    if remaining is not None:
        headers = {
            "RateLimit": f'"rest-complexity-cost";r={remaining};t=60',
            "RateLimit-Policy": POLICY,
            "X-Nautobot-Cost": "4",
        }
    return (status, headers, body)


def scripted(*responses):
    """Return a responder that replies with `responses` in order."""
    queue = deque(responses)
    lock = threading.Lock()

    def responder(_method, _path):
        with lock:
            if queue:
                return queue.popleft()
        return (418, {}, {"detail": "Unexpected request: no scripted response left."})

    return responder


class _StubHandler(BaseHTTPRequestHandler):
    """Record each request and reply with whatever the server's responder returns."""

    def _handle(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length:
            self.rfile.read(length)
        with self.server.lock:
            self.server.requests.append((self.command, self.path))
        status, headers, body = self.server.responder(self.command, self.path)
        payload = json.dumps(body).encode() if body is not None else b""
        self.send_response(status)
        for name, value in headers.items():
            self.send_header(name, value)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    do_GET = do_POST = do_PATCH = do_PUT = do_DELETE = _handle

    def log_message(self, *_args):  # pylint: disable=arguments-differ
        """Keep test output quiet."""


class RateLimitingTestCase(unittest.TestCase):
    """Client behavior when Nautobot returns rate limiting and retryable responses."""

    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), _StubHandler)
        cls.server.lock = threading.Lock()
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f"http://127.0.0.1:{cls.server.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def setUp(self):
        self.server.requests = []
        self.server.responder = scripted()
        sleep_patcher = patch("urllib3.util.retry.time.sleep")
        self.mock_sleep = sleep_patcher.start()
        self.addCleanup(sleep_patcher.stop)

    def script(self, *responses):
        """Reply to the next requests with `responses`, in order."""
        self.server.requests = []
        self.server.responder = scripted(*responses)

    def api(self, **kwargs):
        """Create a pynautobot client pointed at the stub server."""
        return pynautobot.api(self.url, token=TOKEN, **kwargs)

    def assert_throttled_details(self, error):
        """Assert the error kept the 429 response and its rate limit details."""
        self.assertEqual(error.req.status_code, 429)
        self.assertEqual(error.req.headers["Retry-After"], "7")
        self.assertEqual(error.rate_limit.retry_after, 7)
        self.assertEqual(error.rate_limit.remaining, 0)
        self.assertEqual(error.rate_limit.quota, 1000)

    def test_429_raises_request_error_with_retry_after_without_retrying(self):
        nb = self.api()
        self.script(THROTTLED)

        with self.assertRaises(pynautobot.RequestError) as ctx:
            nb.dcim.devices.all()

        self.assert_throttled_details(ctx.exception)
        self.assertNotIsInstance(ctx.exception, pynautobot.RetriesExhaustedError)
        self.assertIn("Request was throttled", str(ctx.exception))
        self.assertEqual(len(self.server.requests), 1)
        self.mock_sleep.assert_not_called()

    def test_429_on_endpoint_get_is_not_treated_as_not_found(self):
        nb = self.api()
        self.script(THROTTLED)

        with self.assertRaises(pynautobot.RequestError) as ctx:
            nb.dcim.devices.get(DEVICE["id"])

        self.assertEqual(ctx.exception.req.status_code, 429)

    def test_429_sleeps_for_retry_after_then_succeeds(self):
        nb = self.api(retries=2)
        self.script(THROTTLED, ok(DEVICE_LIST))

        devices = nb.dcim.devices.all()

        self.assertEqual([device.name for device in devices], ["dev1"])
        self.mock_sleep.assert_called_once_with(7)
        self.assertEqual(len(self.server.requests), 2)

    def test_429_retried_for_every_http_method(self):
        nb = self.api(retries=2)
        cases = [
            ("filter", "GET", ok(DEVICE_LIST), lambda: nb.dcim.devices.filter(name="dev1")),
            ("create", "POST", ok(DEVICE, status=201), lambda: nb.dcim.devices.create(name="dev1")),
            ("update", "PATCH", ok(DEVICE), lambda: nb.dcim.devices.update(DEVICE["id"], {"name": "dev2"})),
            ("delete", "DELETE", (204, {}, None), lambda: nb.dcim.devices.delete([DEVICE["id"]])),
        ]
        for name, method, success, call in cases:
            with self.subTest(name):
                self.script(THROTTLED, success)

                self.assertTrue(call())
                self.assertEqual([request[0] for request in self.server.requests], [method, method])

    def test_5xx_without_retry_after_still_retried(self):
        nb = self.api(retries=2)
        self.script((503, {}, {}), (502, {}, {}), ok(DEVICE_LIST))

        devices = nb.dcim.devices.all()

        self.assertEqual(len(devices), 1)
        self.assertEqual(len(self.server.requests), 3)

    def test_exhausted_retries_raise_error_keeping_429_response(self):
        nb = self.api(retries=2)
        self.script(THROTTLED, THROTTLED, THROTTLED)

        with self.assertRaises(pynautobot.RetriesExhaustedError) as ctx:
            nb.dcim.devices.all()

        self.assertIsInstance(ctx.exception, pynautobot.RequestError)
        self.assertIsInstance(ctx.exception, RequestErrorFromException)
        self.assert_throttled_details(ctx.exception)
        self.assertEqual(len(self.server.requests), 3)

    def test_exhausted_retries_on_status_version_openapi(self):
        nb = self.api(retries=1)
        cases = [
            ("status", nb.status),
            ("version", lambda: nb.version),
            ("openapi", nb.openapi),
        ]
        for name, call in cases:
            with self.subTest(name):
                self.script(THROTTLED, THROTTLED)

                with self.assertRaises(pynautobot.RetriesExhaustedError) as ctx:
                    call()

                self.assert_throttled_details(ctx.exception)

    def test_threaded_pagination_recovers_from_429(self):
        nb = self.api(retries=2, threading=True)
        all_devices = [{"id": f"00000000-0000-0000-0000-00000000000{i}", "name": f"dev{i}"} for i in range(6)]
        throttled_offsets = set()
        lock = threading.Lock()

        def responder(_method, path):
            query = parse_qs(urlparse(path).query)
            offset = int(query.get("offset", ["0"])[0])
            with lock:
                if offset == 4 and offset not in throttled_offsets:
                    throttled_offsets.add(offset)
                    return THROTTLED
            page = {"count": 6, "next": f"{self.url}/api/dcim/devices/?limit=2&offset={offset + 2}"}
            page["results"] = all_devices[offset : offset + 2]
            return ok(page)

        self.server.requests = []
        self.server.responder = responder

        devices = nb.dcim.devices.all()

        self.assertEqual(sorted(device.name for device in devices), [device["name"] for device in all_devices])
        self.assertEqual(throttled_offsets, {4})

    def test_api_rate_limit_tracks_latest_response(self):
        nb = self.api()
        self.script(ok(DEVICE_LIST, remaining=996), ok(DEVICE_LIST, remaining=992))

        nb.dcim.devices.all()
        self.assertEqual(nb.rate_limit.remaining, 996)
        nb.dcim.devices.all()

        self.assertEqual(nb.rate_limit.remaining, 992)
        self.assertEqual(nb.rate_limit.quota, 1000)
        self.assertEqual(nb.rate_limit.cost, 4)
        self.assertEqual(nb.rate_limit.policy, "rest-complexity-cost")

    def test_api_rate_limit_is_none_for_servers_without_rate_limiting(self):
        nb = self.api()
        self.script(ok(DEVICE_LIST))

        devices = nb.dcim.devices.all()

        self.assertEqual(len(devices), 1)
        self.assertIsNone(nb.rate_limit)

    def test_custom_session_with_raising_retry_still_raises_request_error_from_exception(self):
        nb = self.api()
        session = requests.Session()
        adapter = HTTPAdapter(max_retries=Retry(total=1, status_forcelist=[429]))
        session.mount("http://", adapter)
        nb.http_session = session
        self.script(THROTTLED, THROTTLED)

        with self.assertRaises(RequestErrorFromException) as ctx:
            nb.dcim.devices.all()

        self.assertNotIsInstance(ctx.exception, pynautobot.RequestError)
