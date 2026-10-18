"""Tests for StreamingNLG.generate_answer data truncation.

Uses a fake requests module injected via sys.modules so no network is needed.
"""
import sys
import types
import unittest

from enhanced_core.streaming_nlg import StreamingNLG


class _FakeResponse:
    def __init__(self, json_value=None):
        self._json_value = json_value
        self.closed = False

    def raise_for_status(self):
        return None

    def json(self):
        return self._json_value

    def close(self):
        self.closed = True


class _FakeRequests(types.ModuleType):
    def __init__(self, response):
        super().__init__("requests")
        self._response = response
        self.calls = []
        self.exceptions = types.SimpleNamespace(
            RequestException=Exception,
        )

    def post(self, *args, **kwargs):
        self.calls.append(kwargs)
        return self._response


class TestGenerateAnswerTruncation(unittest.TestCase):
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

    def _prompt_of(self, fake):
        self.assertEqual(len(fake.calls), 1)
        payload = fake.calls[0]["json"]
        return payload["messages"][0]["content"]

    def test_large_data_is_truncated(self):
        payload = {"choices": [{"message": {"content": "ok"}}]}
        nlg, fake = self._make(_FakeResponse(json_value=payload))
        big = {"blob": "x" * 6000}
        out = nlg.generate_answer("q", big)
        self.assertEqual(out, "ok")
        prompt = self._prompt_of(fake)
        self.assertIn("... (truncated)", prompt)

    def test_small_data_not_truncated(self):
        payload = {"choices": [{"message": {"content": "ok"}}]}
        nlg, fake = self._make(_FakeResponse(json_value=payload))
        out = nlg.generate_answer("q", {"a": 1})
        self.assertEqual(out, "ok")
        prompt = self._prompt_of(fake)
        self.assertNotIn("(truncated)", prompt)

    def test_truncated_data_still_falls_back_on_bad_response(self):
        nlg, fake = self._make(_FakeResponse(json_value={"id": "x"}))
        big = {"blob": "y" * 6000}
        out = nlg.generate_answer("q", big)
        self.assertEqual(out, "Based on the data, q")
        prompt = self._prompt_of(fake)
        self.assertIn("... (truncated)", prompt)


if __name__ == "__main__":
    unittest.main()
