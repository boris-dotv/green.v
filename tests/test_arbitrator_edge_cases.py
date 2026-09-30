#!/usr/bin/env python3
"""Tests for QueryArbitrator parsing and edge-case handling.

arbitrate() must short-circuit empty/whitespace queries to 'invalid'
without invoking the LLM, and must map the LLM reply A/B/C/D to the
corresponding query_type. Any None, non-string, or unrecognised reply
falls back to 'A' (task) with a warning. These tests pin that observable
contract so a future refactor cannot silently change the safe default or
drop the empty-query guard.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from enhanced_core.arbitrator import QueryArbitrator  # noqa: E402


class RecordingLLM:
    """Fake llm_caller that records calls and returns a fixed reply."""

    def __init__(self, reply):
        self.reply = reply
        self.calls = []

    def __call__(self, prompt, temperature=0.1):
        self.calls.append({"prompt": prompt, "temperature": temperature})
        return self.reply


class TestEmptyQueryGuard(unittest.TestCase):
    def test_empty_string_is_invalid_without_llm_call(self):
        llm = RecordingLLM("A")
        result = QueryArbitrator(llm).arbitrate("")
        self.assertEqual(result.query_type, "invalid")
        self.assertEqual(result.confidence, 1.0)
        self.assertEqual(llm.calls, [])

    def test_whitespace_only_is_invalid_without_llm_call(self):
        llm = RecordingLLM("A")
        result = QueryArbitrator(llm).arbitrate("   \n\t ")
        self.assertEqual(result.query_type, "invalid")
        self.assertEqual(llm.calls, [])


class TestLetterMapping(unittest.TestCase):
    def _arbitrate(self, reply):
        llm = RecordingLLM(reply)
        result = QueryArbitrator(llm).arbitrate("How many employees at ZA Bank?")
        return result, llm

    def test_letter_a_maps_to_task(self):
        result, _ = self._arbitrate("A")
        self.assertEqual(result.query_type, "task")

    def test_letter_b_maps_to_knowledge(self):
        result, _ = self._arbitrate("B")
        self.assertEqual(result.query_type, "knowledge")

    def test_letter_c_maps_to_small_talk(self):
        result, _ = self._arbitrate("C")
        self.assertEqual(result.query_type, "small_talk")

    def test_letter_d_maps_to_invalid(self):
        result, _ = self._arbitrate("D")
        self.assertEqual(result.query_type, "invalid")

    def test_lowercase_and_padded_reply_is_normalised(self):
        result, _ = self._arbitrate("  b  ")
        self.assertEqual(result.query_type, "knowledge")

    def test_confidence_is_fixed_at_0_8(self):
        result, _ = self._arbitrate("A")
        self.assertEqual(result.confidence, 0.8)


class TestFallbackToTask(unittest.TestCase):
    def _arbitrate(self, reply):
        llm = RecordingLLM(reply)
        result = QueryArbitrator(llm).arbitrate("q")
        return result, llm

    def test_none_reply_defaults_to_task(self):
        result, llm = self._arbitrate(None)
        self.assertEqual(result.query_type, "task")
        self.assertEqual(len(llm.calls), 1)

    def test_non_string_reply_defaults_to_task(self):
        result, _ = self._arbitrate(42)
        self.assertEqual(result.query_type, "task")

    def test_unrecognised_letter_defaults_to_task(self):
        result, _ = self._arbitrate("Z")
        self.assertEqual(result.query_type, "task")

    def test_multi_letter_reply_defaults_to_task(self):
        result, _ = self._arbitrate("AB")
        self.assertEqual(result.query_type, "task")


class TestPromptContract(unittest.TestCase):
    def test_query_is_interpolated_into_prompt(self):
        llm = RecordingLLM("A")
        QueryArbitrator(llm).arbitrate("unique-marker-query")
        self.assertEqual(len(llm.calls), 1)
        self.assertIn("unique-marker-query", llm.calls[0]["prompt"])

    def test_history_defaults_to_no_history(self):
        llm = RecordingLLM("A")
        QueryArbitrator(llm).arbitrate("q")
        self.assertIn("No history", llm.calls[0]["prompt"])

    def test_history_is_interpolated_when_provided(self):
        llm = RecordingLLM("A")
        QueryArbitrator(llm).arbitrate("q", history="prior-turn")
        self.assertIn("prior-turn", llm.calls[0]["prompt"])

    def test_temperature_is_low(self):
        llm = RecordingLLM("A")
        QueryArbitrator(llm).arbitrate("q")
        self.assertEqual(llm.calls[0]["temperature"], 0.1)


if __name__ == "__main__":
    unittest.main()
