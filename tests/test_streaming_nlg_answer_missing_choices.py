"""Tests for StreamingNLG.generate_answer when the response JSON is malformed.

Stubs the `requests` module so no network access is required.
"""
import sys
import types
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

_fake_requests = types.ModuleType("requests")


class _RequestException(Exception):
    pass


class _FakeExceptions:
    RequestException = _RequestException


_fake_requests.exceptions = _FakeExceptions()
_fake_requests.post = lambda *a, **k: None
sys.modules["requests"] = _fake_requests

from enhanced_core.streaming_nlg import StreamingNLG  # noqa: E402


class _FakeResponse:
    def __init__(self, payload=None, raise_exc=None):
        self._payload = payload
        self._raise_exc = raise_exc

    def raise_for_status(self):
        if self._raise_exc is not None:
            raise self._raise_exc

    def json(self):
        return self._payload


def _make_nlg():
    return StreamingNLG("http://example.invalid", "key")


class TestGenerateAnswerMissingChoices(unittest.TestCase):
    def setUp(self):
        self._orig_post = _fake_requests.post

    def tearDown(self):
        _fake_requests.post = self._orig_post

    def test_empty_dict_payload_returns_fallback(self):
        nlg = _make_nlg()
        _fake_requests.post = lambda *a, **k: _FakeResponse(payload={})
        out = nlg.generate_answer("q", {"data": 1})
        self.assertIsInstance(out, str)
        self.assertTrue(out)

    def test_choices_missing_message_returns_fallback(self):
        nlg = _make_nlg()
        _fake_requests.post = lambda *a, **k: _FakeResponse(
            payload={"choices": [{}]}
        )
        out = nlg.generate_answer("q", {"data": 1})
        self.assertIsInstance(out, str)
        self.assertTrue(out)

    def test_request_exception_returns_fallback(self):
        nlg = _make_nlg()
        _fake_requests.post = lambda *a, **k: _FakeResponse(
            raise_exc=_RequestException("boom")
        )
        out = nlg.generate_answer("q", {"data": 1})
        self.assertIsInstance(out, str)
        self.assertTrue(out)


if __name__ == "__main__":
    unittest.main()
