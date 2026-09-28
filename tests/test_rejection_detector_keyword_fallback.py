#!/usr/bin/env python3
"""Keyword-heuristic fallback tests for RejectionDetector.

When the LLM reply contains no standalone 0/1 token, should_accept falls
back to scanning the lowercased reply for accept-words ("accept", "yes",
"within scope") and then reject-words ("reject", "no", "out of scope",
"unrelated"), and finally defaults to accepting. These tests pin that
precedence and the safe default; the existing suites only cover the digit
path, the prompt contract and llm_caller errors.
"""

import unittest

from enhanced_core.rejection_detector import RejectionDetector


def _detector(response):
    return RejectionDetector(lambda prompt, temperature=0.1: response)


class TestAcceptKeywords(unittest.TestCase):
    def test_accept_word_accepts(self):
        self.assertTrue(_detector("Accept").should_accept("q"))

    def test_yes_accepts(self):
        self.assertTrue(_detector("yes").should_accept("q"))

    def test_within_scope_accepts(self):
        self.assertTrue(_detector("This is within scope").should_accept("q"))

    def test_keyword_match_is_case_insensitive(self):
        self.assertTrue(_detector("ACCEPT").should_accept("q"))


class TestRejectKeywords(unittest.TestCase):
    def test_reject_word_rejects(self):
        self.assertFalse(_detector("Reject").should_accept("q"))

    def test_no_rejects(self):
        self.assertFalse(_detector("no").should_accept("q"))

    def test_out_of_scope_rejects(self):
        self.assertFalse(_detector("out of scope").should_accept("q"))

    def test_unrelated_rejects(self):
        self.assertFalse(_detector("unrelated topic").should_accept("q"))


class TestPrecedenceAndDefault(unittest.TestCase):
    def test_accept_keyword_wins_over_reject_keyword(self):
        # The accept scan runs first, so a reply mentioning both accepts.
        self.assertTrue(_detector("accept, not reject").should_accept("q"))

    def test_unrecognised_text_defaults_to_accept(self):
        # No digit token and no keyword -> safe default is accept.
        self.assertTrue(_detector("maybe").should_accept("q"))

    def test_whitespace_only_defaults_to_accept(self):
        self.assertTrue(_detector("   ").should_accept("q"))

    def test_digit_token_takes_priority_over_keywords(self):
        # A standalone 0 must reject even when accept-words are present.
        self.assertFalse(_detector("0 (accept)").should_accept("q"))


if __name__ == "__main__":
    unittest.main()
