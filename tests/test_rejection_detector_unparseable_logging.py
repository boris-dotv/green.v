#!/usr/bin/env python3
"""Tests for the RejectionDetector unparseable-output branch.

When the LLM reply contains no bare 0/1 digit token and no accept/reject
keyword, should_accept logs a warning that includes the raw LLM output
(via repr) and falls back to the safe default (Accept). These tests pin
that observable contract so a future refactor cannot silently drop the
diagnostic warning or flip the safe default.
"""

import logging
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from enhanced_core.rejection_detector import RejectionDetector  # noqa: E402


class RecordingLLM:
    """Fake llm_caller that records calls and returns a fixed reply."""

    def __init__(self, reply):
        self.reply = reply
        self.calls = []

    def __call__(self, prompt, temperature=0.1):
        self.calls.append({"prompt": prompt, "temperature": temperature})
        return self.reply


class TestUnparseableLogging(unittest.TestCase):
    def setUp(self):
        self.records = []

        class _Capture(logging.Handler):
            def emit(inner_self, record):
                self.records.append(record)

        self.handler = _Capture()
        self.logger = logging.getLogger("enhanced_core.rejection_detector")
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.DEBUG)

    def tearDown(self):
        self.logger.removeHandler(self.handler)

    def _warnings(self):
        return [r for r in self.records if r.levelno == logging.WARNING]

    def test_unparseable_output_defaults_to_accept(self):
        llm = RecordingLLM("maybe later")
        self.assertTrue(RejectionDetector(llm).should_accept("q"))
        self.assertEqual(len(llm.calls), 1)

    def test_unparseable_output_logs_warning_with_raw_repr(self):
        llm = RecordingLLM("maybe later")
        RejectionDetector(llm).should_accept("q")
        warnings = self._warnings()
        self.assertEqual(len(warnings), 1)
        message = warnings[0].getMessage()
        self.assertIn(repr("maybe later"), message)
        self.assertIn("unparseable", message)

    def test_none_output_logs_warning_with_none_repr(self):
        llm = RecordingLLM(None)
        self.assertTrue(RejectionDetector(llm).should_accept("q"))
        warnings = self._warnings()
        self.assertEqual(len(warnings), 1)
        self.assertIn(repr(None), warnings[0].getMessage())

    def test_parseable_output_does_not_warn(self):
        llm = RecordingLLM("1")
        self.assertTrue(RejectionDetector(llm).should_accept("q"))
        self.assertEqual(self._warnings(), [])

    def test_keyword_output_does_not_warn(self):
        llm = RecordingLLM("reject")
        self.assertFalse(RejectionDetector(llm).should_accept("q"))
        self.assertEqual(self._warnings(), [])


if __name__ == "__main__":
    unittest.main()
