"""Tests for StreamingNLG.generate_streaming input validation and decoding.

Uses a fake requests module injected via sys.modules so no network is needed.
"""
import sys
import types
import unittest

from enhanced_core.streaming_nlg import StreamingNLG


class _FakeResponse:
    def __init__(self, lines):
        self._lines = lines
        self.closed = False

    def raise_for_status(self):
        return None

    def iter_lines(self, decode_unicode=False):
        for line in self._lines:
            yield line

    def close(self):
        self.closed = True


class _FakeRequests(types.ModuleType):
    def __init__(self, response):
        super().__init__("requests")
        self._response = response
        self.calls = 0
        self.exceptions = types.SimpleNamespace(
            RequestException=Exception,
        )

    def post(self, *args, **kwargs):
        self.calls += 1
        return self._response


class TestGenerateStreaming(unittest.TestCase):
    def setUp(self):
        self._saved = sys.modules.get("requests")

    def tearDown(self):
        if self._saved is not None:
            sys.modules["requests"] = self._saved
        else:
            sys.modules.pop("requests", None)

    def _make(self, lines):
        fake = _FakeRequests(_FakeResponse(lines))
        sys.modules["requests"] = fake
        return StreamingNLG("http://example.invalid", "key"), fake

    def test_non_string_prompt_yields_error_without_http(self):
        nlg, fake = self._make([])
        out = list(nlg.generate_streaming(123))
        self.assertEqual(out, ["[Error: Invalid prompt type]"])
        self.assertEqual(fake.calls, 0)

    def test_none_prompt_yields_error_without_http(self):
        nlg, fake = self._make([])
        out = list(nlg.generate_streaming(None))
        self.assertEqual(out, ["[Error: Invalid prompt type]"])
        self.assertEqual(fake.calls, 0)

    def test_empty_prompt_yields_error_without_http(self):
        nlg, fake = self._make([])
        out = list(nlg.generate_streaming("   "))
        self.assertEqual(out, ["[Error: Empty prompt]"])
        self.assertEqual(fake.calls, 0)

    def test_bytes_lines_are_decoded_and_yielded(self):
        lines = [
            b'data: {"choices": [{"delta": {"content": "Hi"}}]}',
            b"",
            b"data: [DONE]",
        ]
        nlg, _ = self._make(lines)
        self.assertEqual(list(nlg.generate_streaming("hello")), ["Hi"])

    def test_str_lines_are_accepted(self):
        lines = [
            'data: {"choices": [{"delta": {"content": "Yo"}}]}',
            "data: [DONE]",
        ]
        nlg, _ = self._make(lines)
        self.assertEqual(list(nlg.generate_streaming("hello")), ["Yo"])

    def test_non_json_line_is_skipped(self):
        lines = [
            b"data: not-json",
            b'data: {"choices": [{"delta": {"content": "Ok"}}]}',
            b"data: [DONE]",
        ]
        nlg, _ = self._make(lines)
        self.assertEqual(list(nlg.generate_streaming("hello")), ["Ok"])

    def test_response_is_closed(self):
        nlg, fake = self._make([b"data: [DONE]"])
        list(nlg.generate_streaming("hello"))
        self.assertTrue(fake._response.closed)


if __name__ == "__main__":
    unittest.main()
