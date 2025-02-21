"""Utilities for tests."""

import json


class Response:
    """Mocked response object for testing."""

    def __init__(self, fixture=None, status_code=200, ok=True, content=None):
        self.status_code = status_code
        self.content = json.dumps(content) if content else self.load_fixture(fixture)
        self.ok = ok

    def load_fixture(self, path):
        """Load fixture from file."""
        with open(f"tests/fixtures/{path}", "r", encoding="utf-8") as f:
            return f.read()

    def json(self):
        """Return json content."""
        return json.loads(self.content)
