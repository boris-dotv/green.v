#!/usr/bin/env python3
"""None / empty-output tests for RejectionDetector.

enhanced_core.rejection_detector guards against a None or empty
llm_caller result before running the digit regex. The existing suites
cover digit parsing, prompt contract, keyword fallback and llm_caller
errors, but not this guard, so a refactor could reintroduce a TypeError
on str(None) or an unintended reject. These tests pin the safe default
(accept) and confirm the caller is still invoked exactly once.
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


class TestNoneOutput(unittest.TestCase):
    def test_none_result_defaults_to_accept(self):
        detector = RejectionDetector(_Recorder(None))
        self.assertTrue(detector.should_accept("q"))

    def test_none_result_does_not_raise(self):
        detector = RejectionDetector(_Recorder(None))
        try:
            detector.should_accept("q")
        except TypeError as exc:  # pragma: no cover - regression guard
            self.fail(f"should_accept raised TypeError on None output: {exc}")

    def test_none_result_still_calls_llm_once(self):
        rec = _Recorder(None)
        RejectionDetector(rec).should_accept("q")
        self.assertEqual(len(rec.calls), 1)


class TestEmptyOutput(unittest.TestCase):
    def test_empty_string_defaults_to_accept(self):
        detector = RejectionDetector(_Recorder(""))
        self.assertTrue(detector.should_accept("q"))

    def test_whitespace_only_defaults_to_accept(self):
        detector = RejectionDetector(_Recorder("   \n\t "))
        self.assertTrue(detector.should_accept("q"))

    def test_empty_output_does_not_raise(self):
        detector = RejectionDetector(_Recorder(""))
        try:
            detector.should_accept("q")
        except Exception as exc:  # pragma: no cover - regression guard
            self.fail(f"should_accept raised on empty output: {exc}")


if __name__ == "__main__":
    unittest.main()
