#!/usr/bin/env python3
"""Tests for QueryRewriter's bad-rewrite overlap guard.

_is_bad_rewrite rejects a rewrite when the number of distinct
characters shared with the original query is less than
len(original) / 4. These tests pin that observable contract so a
future refactor cannot silently weaken the guard and let unrelated
rewrites through.
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


class TestBadRewriteGuard(unittest.TestCase):
    HISTORY = "user: What is ZA Bank's employee size?"

    def _rewrite(self, query, reply):
        llm = RecordingLLM(reply)
        result = QueryRewriter(llm).rewrite(query, self.HISTORY)
        return result, llm

    def test_guard_uses_distinct_chars_not_length(self):
        # original has 4 distinct chars {a,b,c,d}; reply shares only 'a'
        # (overlap 1 < 4/4 = 1.0 is False, so use a longer original)
        query = "abcdabcdabcd"
        reply = "a" * 100
        result, _ = self._rewrite(query, reply)
        self.assertEqual(result, query)

    def test_low_overlap_reply_is_rejected(self):
        query = "How many employees at ZA Bank?"
        reply = "zzzzzzzz"
        result, _ = self._rewrite(query, reply)
        self.assertEqual(result, query)

    def test_high_overlap_reply_is_accepted(self):
        query = "How about WeLab?"
        reply = "How about WeLab Bank?"
        result, _ = self._rewrite(query, reply)
        self.assertEqual(result, "How about WeLab Bank?")

    def test_identical_reply_is_accepted(self):
        query = "How about WeLab?"
        result, _ = self._rewrite(query, query)
        self.assertEqual(result, query)

    def test_guard_boundary_just_below_threshold(self):
        # original distinct chars = 8 -> threshold = 2.0; overlap 1 rejected
        query = "abcdefgh"
        reply = "a"
        result, _ = self._rewrite(query, reply)
        self.assertEqual(result, query)

    def test_guard_boundary_at_threshold(self):
        # original distinct chars = 8 -> threshold = 2.0; overlap 2 accepted
        query = "abcdefgh"
        reply = "ab"
        result, _ = self._rewrite(query, reply)
        self.assertEqual(result, "ab")

    def test_rejected_reply_still_calls_llm_once(self):
        _, llm = self._rewrite("How about WeLab?", "zzzz")
        self.assertEqual(len(llm.calls), 1)

    def test_accepted_reply_is_stripped(self):
        query = "How about WeLab?"
        result, _ = self._rewrite(query, "  How about WeLab Bank?  ")
        self.assertEqual(result, "How about WeLab Bank?")


if __name__ == "__main__":
    unittest.main()
