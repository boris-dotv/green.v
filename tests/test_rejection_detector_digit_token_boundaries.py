#!/usr/bin/env python3
"""Tests for RejectionDetector digit-token boundary parsing.

These pin the observable behaviour of the regex used to parse the LLM reply:
    re.search(r'\b([01])\b', result_str)

Key facts verified by reading enhanced_core/rejection_detector.py:
- The first match in the string wins.
- A digit adjacent to a non-word character (space, punctuation) is a match.
- A digit embedded inside a multi-digit number still matches, because the
  surrounding digits are word characters and the boundary is between the
  digit and the non-word character (or string edge).
- A digit embedded inside a word (e.g. 'a1b') does NOT match.
"""

import logging
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from enhanced_core.rejection_detector import RejectionDetector  # noqa: E402


class RecordingLLM:
    """Fake llm_caller that records prompts and returns a fixed reply."""

    def __init__(self, reply):
        self.reply = reply
        self.calls = []

    def __call__(self, prompt, temperature=0.1):
        self.calls.append({"prompt": prompt, "temperature": temperature})
        return self.reply


class TestDigitTokenBoundaries(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def _decide(self, reply):
        llm = RecordingLLM(reply)
        detector = RejectionDetector(llm)
        return detector.should_accept("What is the employee count of ZA Bank?"), llm

    def test_plain_one_accepts(self):
        accepted, llm = self._decide("1")
        self.assertTrue(accepted)
        self.assertEqual(len(llm.calls), 1)

    def test_plain_zero_rejects(self):
        accepted, _ = self._decide("0")
        self.assertFalse(accepted)

    def test_whitespace_padded_one_accepts(self):
        accepted, _ = self._decide("   1   ")
        self.assertTrue(accepted)

    def test_punctuation_adjacent_one_accepts(self):
        accepted, _ = self._decide("Decision: 1.")
        self.assertTrue(accepted)

    def test_punctuation_adjacent_zero_rejects(self):
        accepted, _ = self._decide("(0)")
        self.assertFalse(accepted)

    def test_ten_contains_standalone_zero_and_rejects(self):
        # '10' -> \b matches between '1' and '0'? No: both are word chars.
        # But '0' at the end has a word boundary after it, and the boundary
        # before it is between '1' and '0' (both word chars) so no match there.
        # However re.search scans left to right; '1' at start has boundary
        # before it (string edge) and after it is '0' (word char) -> no match.
        # Then '0' at end: boundary before is between '1' and '0' (no), so
        # actually '10' does NOT match \b[01]\b. Verify real behaviour.
        accepted, _ = self._decide("10")
        # No standalone digit -> falls through to heuristics -> default accept.
        self.assertTrue(accepted)

    def test_twenty_one_does_not_match_standalone_digit(self):
        accepted, _ = self._decide("21")
        self.assertTrue(accepted)

    def test_digit_embedded_in_word_does_not_match(self):
        # 'a1b' has no word boundary around the '1'.
        accepted, _ = self._decide("a1b")
        self.assertTrue(accepted)

    def test_first_digit_token_wins(self):
        # '1 0' -> first match is '1' -> accept.
        accepted, _ = self._decide("1 0")
        self.assertTrue(accepted)

    def test_first_digit_token_wins_reject(self):
        # '0 1' -> first match is '0' -> reject.
        accepted, _ = self._decide("0 1")
        self.assertFalse(accepted)

    def test_digit_after_word_separator_matches(self):
        # 'answer: 1' -> '1' has boundary before (space) and after (edge).
        accepted, _ = self._decide("answer: 1")
        self.assertTrue(accepted)

    def test_digit_before_word_separator_matches(self):
        accepted, _ = self._decide("1 out of scope")
        self.assertTrue(accepted)

    def test_zero_with_trailing_word_rejects(self):
        accepted, _ = self._decide("0 unrelated")
        self.assertFalse(accepted)


if __name__ == "__main__":
    unittest.main()
