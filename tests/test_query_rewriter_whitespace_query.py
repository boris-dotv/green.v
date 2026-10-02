#!/usr/bin/env python3
"""Tests for QueryRewriter's empty/whitespace query guard.

rewrite() short-circuits before touching history or llm_caller when the
query is falsy or whitespace-only, returning query.strip() for strings
and the value itself for None. These tests pin that contract so a future
refactor cannot start issuing LLM calls for empty input.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from enhanced_core.query_rewriter import QueryRewriter  # noqa: E402


class RecordingLLM:
    """Fake llm_caller that records calls and returns a fixed reply."""

    def __init__(self, reply="rewritten"):
        self.reply = reply
        self.calls = []

    def __call__(self, prompt, temperature=0.3):
        self.calls.append({"prompt": prompt, "temperature": temperature})
        return self.reply


class TestWhitespaceQueryGuard(unittest.TestCase):
    HISTORY = "user: What is ZA Bank's employee size?"

    def test_empty_string_returns_empty_and_skips_llm(self):
        llm = RecordingLLM()
        result = QueryRewriter(llm).rewrite("", self.HISTORY)
        self.assertEqual(result, "")
        self.assertEqual(llm.calls, [])

    def test_whitespace_only_query_is_stripped_and_skips_llm(self):
        llm = RecordingLLM()
        result = QueryRewriter(llm).rewrite("   \t\n  ", self.HISTORY)
        self.assertEqual(result, "")
        self.assertEqual(llm.calls, [])

    def test_none_query_is_returned_as_is(self):
        llm = RecordingLLM()
        result = QueryRewriter(llm).rewrite(None, self.HISTORY)
        self.assertIsNone(result)
        self.assertEqual(llm.calls, [])

    def test_guard_applies_without_history_too(self):
        llm = RecordingLLM()
        result = QueryRewriter(llm).rewrite("   ", "")
        self.assertEqual(result, "")
        self.assertEqual(llm.calls, [])

    def test_padded_query_is_passed_through_to_llm(self):
        llm = RecordingLLM("How about WeLab Bank?")
        result = QueryRewriter(llm).rewrite("  How about WeLab?  ", self.HISTORY)
        self.assertEqual(result, "How about WeLab Bank?")
        self.assertEqual(len(llm.calls), 1)
        self.assertIn("How about WeLab?", llm.calls[0]["prompt"])


if __name__ == "__main__":
    unittest.main()
