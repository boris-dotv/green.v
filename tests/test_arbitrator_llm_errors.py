#!/usr/bin/env python3
"""Tests for QueryArbitrator behaviour when llm_caller fails.

arbitrate() has no try/except around self.llm_caller, so any exception
raised by the LLM call propagates to the caller unchanged. These tests
pin that observable contract so a future refactor cannot silently
swallow LLM failures and hide errors behind the safe 'A' default.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from enhanced_core.arbitrator import QueryArbitrator  # noqa: E402


class RaisingLLM:
    """Fake llm_caller that records calls and raises a fixed exception."""

    def __init__(self, exc):
        self.exc = exc
        self.calls = []

    def __call__(self, prompt, temperature=0.1):
        self.calls.append({"prompt": prompt, "temperature": temperature})
        raise self.exc


class TestLLMExceptionPropagation(unittest.TestCase):
    def test_runtime_error_propagates(self):
        llm = RaisingLLM(RuntimeError("boom"))
        with self.assertRaises(RuntimeError):
            QueryArbitrator(llm).arbitrate("How many employees at ZA Bank?")
        self.assertEqual(len(llm.calls), 1)

    def test_value_error_propagates(self):
        llm = RaisingLLM(ValueError("bad prompt"))
        with self.assertRaises(ValueError):
            QueryArbitrator(llm).arbitrate("q")

    def test_timeout_error_propagates(self):
        llm = RaisingLLM(TimeoutError("timed out"))
        with self.assertRaises(TimeoutError):
            QueryArbitrator(llm).arbitrate("q")

    def test_exception_message_is_preserved(self):
        llm = RaisingLLM(RuntimeError("unique-marker-error"))
        try:
            QueryArbitrator(llm).arbitrate("q")
        except RuntimeError as exc:
            self.assertIn("unique-marker-error", str(exc))
        else:
            self.fail("RuntimeError was not raised")

    def test_empty_query_guard_runs_before_llm_call(self):
        llm = RaisingLLM(RuntimeError("should not be called"))
        result = QueryArbitrator(llm).arbitrate("")
        self.assertEqual(result.query_type, "invalid")
        self.assertEqual(llm.calls, [])


if __name__ == "__main__":
    unittest.main()
