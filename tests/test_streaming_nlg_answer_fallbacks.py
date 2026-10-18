"""Tests for StreamingNLG.generate_answer fallback paths.

Uses a fake requests module injected via sys.modules so no network is needed.
"""
import sys
import types
import unittest

from enhanced_core.streaming_nlg import StreamingNLG


class _FakeResponse:
    def __init__(self, json_value=None, json_error=None, status_error=None):
        self._json_value = json_value
        self._json_error = json_error
        self._status_error = status_error
        self.closed = False

    def raise_for_status(self):
        if self._status_error is not None:
            raise self._status_error

    def json(self):
        if self._json_error is not None:
            raise self._json_error
        return self._json_value

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


class TestGenerateAnswerFallbacks(unittest.TestCase):
    def setUp(self):
        self._saved = sys.modules.get("requests")

    def tearDown(self):
        if self._saved is not None:
            sys.modules["requests"] = self._saved
        else:
            sys.modules.pop("requests", None)

    def _make(self, response):
        fake = _FakeRequests(response)
        sys.modules["requests"] = fake
        return StreamingNLG("http://example.invalid", "key"), fake

    def test_missing_choices_returns_fallback(self):
        nlg, fake = self._make(_FakeResponse(json_value={"id": "x"}))
        out = nlg.generate_answer("ZA Bank employees", {"employees": 100})
        self.assertEqual(out, "Based on the data, ZA Bank employees")
        self.assertEqual(fake.calls, 1)

    def test_empty_choices_returns_fallback(self):
        nlg, fake = self._make(_FakeResponse(json_value={"choices": []}))
        out = nlg.generate_answer("q", {"a": 1})
        self.assertEqual(out, "Based on the data, q")
        self.assertEqual(fake.calls, 1)

    def test_json_decode_error_returns_fallback(self):
        nlg, fake = self._make(_FakeResponse(json_error=ValueError("bad json")))
        out = nlg.generate_answer("q", {"a": 1})
        self.assertEqual(out, "Based on the data, q")
        self.assertEqual(fake.calls, 1)

    def test_raise_for_status_error_returns_fallback(self):
        nlg, fake = self._make(_FakeResponse(status_error=RuntimeError("boom")))
        out = nlg.generate_answer("q", {"a": 1})
        self.assertEqual(out, "Based on the data, q")
        self.assertEqual(fake.calls, 1)

    def test_valid_choices_returns_content(self):
        payload = {"choices": [{"message": {"content": "Answer text"}}]}
        nlg, fake = self._make(_FakeResponse(json_value=payload))
        self.assertEqual(nlg.generate_answer("q", {"a": 1}), "Answer text")
        self.assertEqual(fake.calls, 1)

    def test_invalid_data_skips_http(self):
        nlg, fake = self._make(_FakeResponse(json_value={}))
        self.assertEqual(nlg.generate_answer("q", None), "抱歉，查询结果为空或格式不正确。")
        self.assertEqual(fake.calls, 0)

    def test_empty_query_skips_http(self):
        nlg, fake = self._make(_FakeResponse(json_value={}))
        self.assertEqual(nlg.generate_answer("   ", {"a": 1}), "抱歉，查询内容为空。")
        self.assertEqual(fake.calls, 0)


if __name__ == "__main__":
    unittest.main()
