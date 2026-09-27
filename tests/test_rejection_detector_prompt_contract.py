#!/usr/bin/env python3
"""Prompt-contract and digit-boundary tests for RejectionDetector.

enhanced_core.rejection_detector only needs the standard library and an
injected llm_caller, so these tests run without network or heavy deps.
They lock in the prompt template (scope keywords, query interpolation,
temperature) and the \\b([01])\\b boundary rule used to parse the LLM
reply, which the existing suites do not cover.
"""

import unittest

from enhanced_core.rejection_detector import RejectionDetector


class _Recorder:
    """Callable that records prompts and returns a canned response."""

    def __init__(self, response):
        self.response = response
        self.calls = []

    def __call__(self, prompt, temperature=None):
        self.calls.append({"prompt": prompt, "temperature": temperature})
        return self.response


class TestPromptContract(unittest.TestCase):
    def test_prompt_lists_accept_and_reject_scopes(self):
        rec = _Recorder("1")
        RejectionDetector(rec).should_accept("q")
        prompt = rec.calls[0]["prompt"]
        self.assertIn("ACCEPT", prompt)
        self.assertIn("REJECT", prompt)
        self.assertIn("Output ONLY: 1 (accept) or 0 (reject)", prompt)

    def test_prompt_embeds_query_verbatim(self):
        rec = _Recorder("1")
        query = "Compare shareholder concentration between ZA Bank and WeLab Bank"
        RejectionDetector(rec).should_accept(query)
        self.assertIn(f"Query: {query}", rec.calls[0]["prompt"])

    def test_prompt_uses_low_temperature(self):
        rec = _Recorder("1")
        RejectionDetector(rec).should_accept("q")
        self.assertEqual(rec.calls[0]["temperature"], 0.1)

    def test_llm_caller_invoked_once_per_query(self):
        rec = _Recorder("1")
        detector = RejectionDetector(rec)
        detector.should_accept("first")
        detector.should_accept("second")
        self.assertEqual(len(rec.calls), 2)
        self.assertIn("first", rec.calls[0]["prompt"])
        self.assertIn("second", rec.calls[1]["prompt"])


class TestDigitBoundaries(unittest.TestCase):
    def test_multi_digit_numbers_are_not_treated_as_decisions(self):
        # \\b([01])\\b must not match a digit inside a longer number, so
        # these fall through to the safe default of accepting.
        for response in ("10", "01", "100", "2", "42"):
            with self.subTest(response=response):
                detector = RejectionDetector(_Recorder(response))
                self.assertTrue(detector.should_accept("q"))

    def test_digit_surrounded_by_punctuation_is_parsed(self):
        for response, expected in (("1.", True), ("(0)", False), ("[1]", True), ("0,", False)):
            with self.subTest(response=response):
                detector = RejectionDetector(_Recorder(response))
                self.assertEqual(detector.should_accept("q"), expected)

    def test_first_digit_token_wins(self):
        # re.search returns the leftmost match, so "1 ... 0" accepts.
        detector = RejectionDetector(_Recorder("1 then 0"))
        self.assertTrue(detector.should_accept("q"))
        detector = RejectionDetector(_Recorder("0 then 1"))
        self.assertFalse(detector.should_accept("q"))

    def test_non_string_result_is_stringified(self):
        detector = RejectionDetector(_Recorder(1))
        self.assertTrue(detector.should_accept("q"))
        detector = RejectionDetector(_Recorder(0))
        self.assertFalse(detector.should_accept("q"))


if __name__ == "__main__":
    unittest.main()
