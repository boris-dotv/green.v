#!/usr/bin/env python3
"""Tests for QueryRewriter handling of non-string llm_caller replies.

rewrite() feeds the llm_caller result into _is_bad_rewrite, which calls
len(set(rewritten)) and set(rewritten).intersection(original). A model
that returns a list, dict, int or None would previously raise TypeError
and crash the rewrite step. These tests pin the hardened contract: any
non-string reply is logged and the original query is returned unchanged,
and the llm_caller is still invoked exactly once.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from enhanced_core.query_rewriter import QueryRewriter  # noqa: E402


class RecordingLLM:
    """Fake llm_caller that records calls and returns a fixed reply."""

    def __init__(self, reply):
        self.reply = reply
        self.calls = []

    def __call__(self, prompt, temperature=0.3):
        self.calls.append({"prompt": prompt, "temperature": temperature})
        return self.reply


class TestNonStringReplyFallsBack(unittest.TestCase):
    QUERY = "How many employees at ZA Bank?"
    HISTORY = "user: hi\nassistant: hello"

    def _rewrite(self, reply):
        llm = RecordingLLM(reply)
        result = QueryRewriter(llm).rewrite(self.QUERY, self.HISTORY)
        return result, llm

    def test_list_reply_returns_original_query(self):
        result, llm = self._rewrite(["How many employees at ZA Bank?"])
        self.assertEqual(result, self.QUERY)
        self.assertEqual(len(llm.calls), 1)

    def test_dict_reply_returns_original_query(self):
        result, _ = self._rewrite({"query": "x"})
        self.assertEqual(result, self.QUERY)

    def test_int_reply_returns_original_query(self):
        result, _ = self._rewrite(42)
        self.assertEqual(result, self.QUERY)

    def test_none_reply_returns_original_query(self):
        result, _ = self._rewrite(None)
        self.assertEqual(result, self.QUERY)

    def test_empty_string_reply_returns_original_query(self):
        result, _ = self._rewrite("")
        self.assertEqual(result, self.QUERY)

    def test_whitespace_only_reply_returns_original_query(self):
        result, _ = self._rewrite("   ")
        self.assertEqual(result, self.QUERY)

    def test_non_string_reply_does_not_raise(self):
        for reply in ([], {}, 0, 3.14, object()):
            with self.subTest(reply=reply):
                result, _ = self._rewrite(reply)
                self.assertEqual(result, self.QUERY)

    def test_temperature_is_passed_through(self):
        _, llm = self._rewrite(["x"])
        self.assertEqual(llm.calls[0]["temperature"], 0.3)

    def test_prompt_contains_query_and_history(self):
        _, llm = self._rewrite(["x"])
        prompt = llm.calls[0]["prompt"]
        self.assertIn(self.QUERY, prompt)
        self.assertIn(self.HISTORY, prompt)


class TestGoodStringReplyStillRewrites(unittest.TestCase):
    QUERY = "How about WeLab?"
    HISTORY = "user: What is ZA Bank's employee size?"

    def test_string_reply_is_returned_stripped(self):
        llm = RecordingLLM("  How about WeLab Bank?  ")
        result = QueryRewriter(llm).rewrite(self.QUERY, self.HISTORY)
        self.assertEqual(result, "How about WeLab Bank?")


class TestNoHistoryShortCircuit(unittest.TestCase):
    def test_no_history_skips_llm_call(self):
        llm = RecordingLLM("should not be used")
        result = QueryRewriter(llm).rewrite("q", "")
        self.assertEqual(result, "q")
        self.assertEqual(llm.calls, [])


if __name__ == "__main__":
    unittest.main()
