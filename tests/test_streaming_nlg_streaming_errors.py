"""Tests for StreamingNLG.generate_streaming error and success paths.

Stubs the `requests` module so no network access is required.
"""
import sys
import types
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Build a fake requests module with the pieces streaming_nlg uses.
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
    def __init__(self, lines=None, raise_exc=None):
        self._lines = lines or []
        self._raise_exc = raise_exc
        self.closed = False

    def raise_for_status(self):
        if self._raise_exc is not None:
            raise self._raise_exc

    def iter_lines(self, decode_unicode=False):
        for line in self._lines:
            yield line

    def close(self):
        self.closed = True


def _make_nlg():
    return StreamingNLG("http://example.invalid", "key")


class TestGenerateStreamingErrors(unittest.TestCase):
    def setUp(self):
        self._orig_post = _fake_requests.post

    def tearDown(self):
        _fake_requests.post = self._orig_post

    def test_non_string_prompt_yields_error(self):
        nlg = _make_nlg()
        out = list(nlg.generate_streaming(None))
        self.assertEqual(out, ["[Error: Invalid prompt type]"])

    def test_empty_prompt_yields_error(self):
        nlg = _make_nlg()
        out = list(nlg.generate_streaming("   "))
        self.assertEqual(out, ["[Error: Empty prompt]"])

    def test_request_exception_yields_error_and_closes(self):
        nlg = _make_nlg()
        resp = _FakeResponse(raise_exc=_RequestException("boom"))
        _fake_requests.post = lambda *a, **k: resp
        out = list(nlg.generate_streaming("hello"))
        self.assertEqual(len(out), 1)
        self.assertTrue(out[0].startswith("[Error: "))
        self.assertIn("boom", out[0])
        self.assertTrue(resp.closed)

    def test_successful_stream_yields_content(self):
        nlg = _make_nlg()
        lines = [
            b'data: {"choices": [{"delta": {"content": "hi"}}]}',
            b"",
            b"data: [DONE]",
        ]
        resp = _FakeResponse(lines=lines)
        _fake_requests.post = lambda *a, **k: resp
        out = list(nlg.generate_streaming("hello"))
        self.assertEqual(out, ["hi"])
        self.assertTrue(resp.closed)


if __name__ == "__main__":
    unittest.main()
